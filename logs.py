import os
import sys
import argparse
import traceback

try:
    import paramiko
except ImportError:
    paramiko = None

# Re-use the same targets and directories as deploy.py
TARGETS = {
    "sshLocal": {
        "host": "192.168.1.50",
        "port": 22,
        "user": "vega",
        "password": "1010",
        "label": "LAN (same Wi-Fi as the server)",
    },
    "sshPublic": {
        "host": "100.107.83.28",
        "port": 22009,
        "user": "vega",
        "password": "1010",
        "label": "Tailscale (public IP 100.107.83.28)",
    },
}

REMOTE_DIR_DEV = "/home/vega/artha-dev"
REMOTE_DIR_PROD = "/home/vega/artha"

def get_password(target_name):
    return os.environ.get("DEPLOY_PASSWORD") or TARGETS[target_name]["password"]

def connect_ssh(host, port, user, password):
    if paramiko is None:
        print("ERROR: paramiko (the SSH library) is not installed.")
        print("Install it with:  pip install paramiko")
        sys.exit(1)
        
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"Connecting to {user}@{host}:{port}...")
    try:
        ssh.connect(host, port=port, username=user, password=password, timeout=15)
    except Exception as exc:
        print(f"Failed to connect: {exc}")
        sys.exit(1)
    print("Connected.\n")
    return ssh

def main():
    parser = argparse.ArgumentParser(description="View live logs for Artha Billing Application.")
    
    # Target groups
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--local", action="store_true", help="View logs locally.")
    group.add_argument("--sshLocal", action="store_true", help="View logs via SSH on LAN.")
    group.add_argument("--sshPublic", action="store_true", help="View logs via SSH on Tailscale IP.")
    
    # Env groups
    env_group = parser.add_mutually_exclusive_group()
    env_group.add_argument("--dev", action="store_true", help="View development environment logs.")
    env_group.add_argument("--prod", action="store_true", help="View production environment logs.")
    
    parser.add_argument("service", nargs="?", default="", help="Optional specific service to view (e.g. backend, frontend).")
    
    args = parser.parse_args()

    # Determine environment and remote dir
    env = "prod" if args.prod else "dev"
    remote_dir = REMOTE_DIR_PROD if env == "prod" else REMOTE_DIR_DEV
    compose_file = "compose.prod.yml" if env == "prod" else "compose.dev.yml"
    
    # Determine target
    target_name = "local" if args.local else ("sshPublic" if args.sshPublic else "sshLocal")
    
    # Build the docker compose logs command
    cmd = f"cd {remote_dir} && docker compose -f {compose_file} logs -f --tail=100 {args.service}"
    
    print("=" * 50)
    print(f" MODE: {env.upper()}")
    print(f" TARGET: {target_name.upper()}")
    if args.service:
        print(f" SERVICE: {args.service}")
    print("=" * 50)
    
    if target_name == "local":
        print(f"Running locally: {cmd}")
        try:
            os.system(cmd)
        except KeyboardInterrupt:
            print("\nExiting logs.")
        sys.exit(0)
        
    cfg = TARGETS[target_name]
    ssh = connect_ssh(cfg["host"], cfg["port"], cfg["user"], get_password(target_name))
    
    print(f"Running: {cmd}")
    print("Streaming logs (Press Ctrl+C to stop)...\n")
    print("-" * 50)
    
    try:
        # get_pty=True helps avoid output buffering issues with docker compose
        _, stdout, stderr = ssh.exec_command(cmd, get_pty=True)
        
        while True:
            data = stdout.channel.recv(4096)
            if not data:
                break
            sys.stdout.buffer.write(data)
            sys.stdout.flush()
            
    except KeyboardInterrupt:
        print("\nStopping log stream...")
    except Exception as exc:
        print(f"\nConnection lost or error: {exc}")
    finally:
        try:
            ssh.close()
        except:
            pass
        print("Disconnected.")

if __name__ == "__main__":
    main()
