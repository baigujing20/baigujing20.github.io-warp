import requests
import json
import secrets
import base64
import uuid
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization

class CloudflareRegistrationBase:
    def __init__(self):
        self.api_url = "https://api.cloudflareclient.com/v0a4471"
        self.headers = {
            "User-Agent": "WARP for Android",
            "CF-Client-Version": "a-6.35-4471",
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json"
        }
        self.timeout = 15

    def register_device(self, public_key):
        tos = datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        registration = {
            "key": public_key,
            "install_id": str(uuid.uuid4()),
            "fcm_token": "",
            "tos": tos,
            "model": "PC",
            "serial_number": secrets.token_hex(8),
            "os_version": "",
            "key_type": "curve25519",
            "tunnel_type": "wireguard"
        }
        response = requests.post(
            f"{self.api_url}/reg",
            headers=self.headers,
            json=registration,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()


class WireGuardConfigGenerator(CloudflareRegistrationBase):
    """注册 Cloudflare WireGuard 设备并生成标准 WireGuard 配置。"""

    def __init__(self, output_file="config.conf"):
        super().__init__()
        self.output_file = output_file

    @staticmethod
    def generate_private_key():
        private_key = x25519.X25519PrivateKey.generate()
        return base64.b64encode(private_key.private_bytes(
            serialization.Encoding.Raw,
            serialization.PrivateFormat.Raw,
            serialization.NoEncryption()
        )).decode()

    @staticmethod
    def _with_prefix(address, prefix):
        address = str(address).strip()
        if not address:
            return ""
        return address if "/" in address else f"{address}/{prefix}"

    @staticmethod
    def _format_endpoint(endpoint):
        endpoint = str(endpoint).strip()
        if not endpoint:
            raise ValueError("注册响应中没有有效的 peer.endpoint")
        if endpoint.startswith("[") or ":" not in endpoint:
            return endpoint
        # IPv6 端点在 WireGuard 配置文件中需要使用方括号
        host, port = endpoint.rsplit(":", 1)
        if ":" not in host:
            return endpoint
        if "]" not in host:
            return f"[{host}]:{port}"
        return endpoint

    @staticmethod
    def _get_endpoint(endpoint_data):
        if isinstance(endpoint_data, dict):
            for field in ("host", "v4", "v6"):
                endpoint = endpoint_data.get(field)
                if endpoint:
                    return endpoint
        elif endpoint_data:
            return endpoint_data
        raise ValueError("注册响应中没有有效的 peer.endpoint")

    @classmethod
    def render_config(cls, response, private_key):
        config = response.get("config", {})
        interface = config.get("interface", {})
        addresses = interface.get("addresses", {})
        peers = config.get("peers", [])
        if not peers:
            raise ValueError("注册响应中没有 WireGuard peer")

        peer = peers[0]
        peer_key = peer.get("public_key") or peer.get("publicKey") or peer.get("key")
        if not peer_key:
            raise ValueError("注册响应中没有 peer 公钥")
        endpoint_data = peer.get("endpoint", {})
        endpoint = cls._format_endpoint(cls._get_endpoint(endpoint_data))
        client_id = config.get("client_id")
        if not client_id:
            raise ValueError("注册响应中没有 config.client_id")

        ipv4 = cls._with_prefix(addresses.get("v4", ""), 32)
        ipv6 = cls._with_prefix(addresses.get("v6", ""), 128)
        interface_addresses = ", ".join(item for item in (ipv4, ipv6) if item)
        allowed_ips = peer.get("allowed_ips") or peer.get("allowedIPs") or ["0.0.0.0/0", "::/0"]
        allowed_ips = ", ".join(str(item) for item in allowed_ips)
        dns = interface.get("dns") or config.get("dns") or "1.1.1.1"
        dns = ", ".join(str(item) for item in dns) if isinstance(dns, list) else str(dns)
        mtu = interface.get("mtu") or config.get("mtu") or 1280
        try:
            reserved = list(base64.b64decode(client_id, validate=True))
        except (ValueError, TypeError) as error:
            raise ValueError("config.client_id 不是有效的 Base64") from error
        if not reserved:
            raise ValueError("config.client_id 解码后为空")

        return "\n".join([
            "[Interface]",
            f"PrivateKey = {private_key}",
            f"Address = {interface_addresses}",
            f"DNS = {dns}",
            f"MTU = {mtu}",
            "[Peer]",
            f"PublicKey = {peer_key}",
            f"AllowedIPs = {allowed_ips}",
            f"Endpoint = {endpoint}",
            f"Reserved = {json.dumps(reserved, separators=(', ', ':'))}",
        ])

    def run(self):
        private_key = self.generate_private_key()
        private_key_obj = x25519.X25519PrivateKey.from_private_bytes(
            base64.b64decode(private_key)
        )
        public_key = base64.b64encode(private_key_obj.public_key().public_bytes(
            serialization.Encoding.Raw,
            serialization.PublicFormat.Raw
        )).decode()
        print("[*] 正在向 Cloudflare 注册 WireGuard 设备...")
        try:
            response_data = self.register_device(public_key)
            # print(response_data)
            warp_plus = response_data.get("account", {}).get("warp_plus", False)
            print(f"[OK] Warp+ 账户: {warp_plus}, Quota(配额): 0")
            config_text = self.render_config(response_data, private_key)
        except (requests.RequestException, ValueError, KeyError, TypeError) as error:
            print(f"[-] WireGuard 注册失败: {error}")
            return
        print("[OK] 注册成功！以下是生成的配置：\n")
        print(config_text)
        with open(self.output_file, "w") as config_file:
            config_file.write(config_text)
        print(f"\n[!] WireGuard 配置已保存到 {self.output_file}")


if __name__ == "__main__":
    WireGuardConfigGenerator().run()
