import requests
import time
from datetime import datetime

# Configuration
LOCAL_API_URL = "http://127.0.0.1:5000"
SYNC_INTERVAL = 20  # seconds
DELAY_BETWEEN_SYNCS = 2  # seconds

def sync_external():
    """Sync from external API to local database."""
    try:
        print(f"🌐 Starting external sync at {datetime.now().strftime('%H:%M:%S')}")
        response = requests.post(f"{LOCAL_API_URL}/api/v1/sync-external", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ External sync completed: {data.get('created', 0)} created, {data.get('updated', 0)} updated")
            return True
        else:
            print(f"❌ External sync failed: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ External sync timeout")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ External sync error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in external sync: {e}")
        return False

def sync_to_collar():
    """Sync from local database to collar API."""
    try:
        print(f"🔄 Starting collar sync at {datetime.now().strftime('%H:%M:%S')}")
        response = requests.post(f"{LOCAL_API_URL}/api/v1/sync-to-collar", timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Collar sync completed: {data.get('sent', 0)} sent, {data.get('errors', 0)} errors")
            return True
        else:
            print(f"❌ Collar sync failed: {response.status_code} - {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Collar sync timeout")
        return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Collar sync error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in collar sync: {e}")
        return False

def run_sync_cycle():
    """Run a complete sync cycle: external -> wait -> collar."""
    print("=" * 60)
    print(f"🚀 Starting sync cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Step 1: Sync from external API
    external_success = sync_external()
    
    # Step 2: Wait 2 seconds
    print(f"⏳ Waiting {DELAY_BETWEEN_SYNCS} seconds...")
    time.sleep(DELAY_BETWEEN_SYNCS)
    
    # Step 3: Sync to collar API
    collar_success = sync_to_collar()
    
    # Summary
    if external_success and collar_success:
        print("✅ Complete sync cycle successful")
    elif external_success:
        print("⚠️  Sync cycle partially successful (external ok, collar failed)")
    elif collar_success:
        print("⚠️  Sync cycle partially successful (external failed, collar ok)")
    else:
        print("❌ Complete sync cycle failed")
    
    print("=" * 60)

def run_continuous_sync():
    """Run continuous sync cycles every 20 seconds."""
    print("🎯 Starting continuous API synchronization...")
    print(f"⏰ Sync interval: {SYNC_INTERVAL} seconds")
    print(f"⏱️  Delay between syncs: {DELAY_BETWEEN_SYNCS} seconds")
    print(f"📡 Local API: {LOCAL_API_URL}")
    print("🔄 Sync order: external → collar")
    print("\nPress Ctrl+C to stop...\n")
    
    cycle_count = 0
    
    while True:
        try:
            cycle_count += 1
            print(f"📊 Cycle #{cycle_count}")
            
            run_sync_cycle()
            
            print(f"😴 Sleeping for {SYNC_INTERVAL} seconds until next cycle...\n")
            time.sleep(SYNC_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n🛑 Synchronization stopped by user")
            print(f"📈 Total cycles completed: {cycle_count}")
            break
        except Exception as e:
            print(f"💥 Unexpected error in sync cycle: {e}")
            print("⏳ Waiting before retry...")
            time.sleep(SYNC_INTERVAL)

def run_single_cycle():
    """Run a single sync cycle for testing."""
    print("🧪 Running single sync cycle test...")
    run_sync_cycle()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Run single cycle for testing
        run_single_cycle()
    else:
        # Run continuous sync
        run_continuous_sync()

