import requests
import json
import secrets
import base64
import uuid
from datetime import datetime, timezone
from cryptography.hazmat.primitives.asymmetric import x25519, ec
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

    def register_device(self, public_key, tunnel_type="wireguard"):
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
            "tunnel_type": tunnel_type
        }
        response = requests.post(
            f"{self.api_url}/reg",
            headers=self.headers,
            json=registration,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()


class MasqueConfigGenerator(CloudflareRegistrationBase):
    def __init__(self, output_file="config.json"):
        super().__init__()
        # Cloudflare 默认的 MASQUE 节点公钥 (固定值)
        self.CF_ENDPOINT_PUB_KEY = (
            "-----BEGIN PUBLIC KEY-----\n"
            "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEIaU7MToJm9NKp8YfGxR6r+/h4mcG\n"
            "7SxI8tsW8OR1A5tv/zCzVbCRRh2t87/kxnP6lAy0lkr7qYwu+ox+k3dr6w==\n"
            "-----END PUBLIC KEY-----\n"
        )
        self.output_file = output_file

    def generate_keys(self):
        """生成 WireGuard 注册用的 WG 密钥和 MASQUE 用的 P-256 密钥"""
        # WireGuard Key
        wg_priv_obj = x25519.X25519PrivateKey.generate()
        wg_pub = base64.b64encode(wg_priv_obj.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)).decode()

        # P-256 Key (MASQUE)
        ec_priv_obj = ec.generate_private_key(ec.SECP256R1())
        # usque sends the public key as ASN.1 PKIX/SubjectPublicKeyInfo DER.
        ec_pub = base64.b64encode(ec_priv_obj.public_key().public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )).decode()
        # 导出为 SEC1/传统 EC 私钥
        ec_priv = base64.b64encode(ec_priv_obj.private_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )).decode()

        return wg_pub, ec_pub, ec_priv

    def run(self):
        wg_pub, ec_pub, ec_priv = self.generate_keys()

        # 1. 基础注册
        print("[*] 正在向 Cloudflare 注册新设备...")
        try:
            res1 = self.register_device(wg_pub)
        except requests.RequestException as e:
            print(f"[-] 注册请求失败: {e}")
            return

        try:
            device_id = res1["id"]
            token = res1["token"]
        except (ValueError, KeyError, TypeError) as e:
            print(f"[-] 注册响应格式无效: {e}")
            return

        # 2. 升级到 MASQUE
        auth_headers = {**self.headers, "Authorization": f"Bearer {token}"}
        enroll_data = {
            "key": ec_pub,
            "key_type": "secp256r1",
            "tunnel_type": "masque",
            "name": f"MASQUE-{secrets.token_hex(4)}"
        }

        print(f"[*] 正在开启 MASQUE 协议并获取 IP 分配...")
        try:
            r2 = requests.patch(
                f"{self.api_url}/reg/{device_id}",
                headers=auth_headers,
                json=enroll_data,
                timeout=self.timeout
            )
        except requests.RequestException as e:
            print(f"[-] MASQUE 升级请求失败: {e}")
            return
        if r2.status_code != 200:
            print(f"[-] 升级失败: {r2.text}")
            return

        try:
            res2 = r2.json()
            # print(res2)
            warp_plus = res2.get("account", {}).get("warp_plus", False)
            print(f"[OK] Warp+ 账户: {warp_plus}, quota(配额): 0")
        except ValueError as e:
            print(f"[-] 升级响应格式无效: {e}")
            return

        try:
            peer = res2["config"]["peers"][0]
            endpoint = peer["endpoint"]
            endpoint_v4 = endpoint["v4"].rsplit(":", 1)[0]
            endpoint_v6 = endpoint["v6"]
            if endpoint_v6.startswith("[") and "]" in endpoint_v6:
                endpoint_v6 = endpoint_v6[1:endpoint_v6.index("]")]
            elif endpoint_v6.endswith(":0"):
                endpoint_v6 = endpoint_v6[:-2]
        except (KeyError, IndexError, TypeError, AttributeError) as e:
            print(f"[-] 注册响应缺少有效的 MASQUE 端点: {e}")
            return

        # 3. 构造输出的格式
        config_output = {
            "private_key": ec_priv,
            "endpoint_v4": endpoint_v4,
            "endpoint_v6": endpoint_v6,
            "endpoint_h2_v4": endpoint_v4,
            "endpoint_h2_v6": endpoint_v6,
            "endpoint_pub_key": self.CF_ENDPOINT_PUB_KEY,
            "license": res2.get("account", {}).get("license", ""),
            "id": device_id,
            "access_token": token,
            "ipv4": res2.get("config", {}).get("interface", {}).get("addresses", {}).get("v4", ""),
            "ipv6": res2.get("config", {}).get("interface", {}).get("addresses", {}).get("v6", "")
        }

        print("[OK] 注册成功！以下是生成的配置：\n")
        print(json.dumps(config_output, indent=2))

        with open(self.output_file, "w") as f:
            json.dump(config_output, f, indent=2)
        print(f"\n[!] masque 配置已保存到 {self.output_file}")


if __name__ == "__main__":
    MasqueConfigGenerator().run()
