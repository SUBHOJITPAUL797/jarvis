"""
Test script for Jarvis AI Complete Application
Tests all features to ensure everything works
"""

import os
import json
import time
from datetime import datetime

def test_endpoint(url, method='GET', data=None, headers=None):
    """Test an API endpoint"""
    import requests
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        else:
            return False, "Unsupported method"
        
        return response.status_code, response.json() if response.content else None
    except Exception as e:
        return False, str(e)

def run_tests():
    """Run all tests"""
    base_url = "http://localhost:10000"
    results = []
    
    print("🧪 Starting Jarvis AI Complete Tests...\n")
    
    # Test 1: Health Check
    print("1️⃣ Testing health endpoint...")
    status, data = test_endpoint(f"{base_url}/health")
    if status == 200:
        print("✅ Health check passed")
        results.append(("Health Check", "PASS"))
    else:
        print("❌ Health check failed")
        results.append(("Health Check", "FAIL"))
    
    # Test 2: Main Page
    print("\n2️⃣ Testing main page...")
    status, _ = test_endpoint(base_url)
    if status == 200:
        print("✅ Main page loads")
        results.append(("Main Page", "PASS"))
    else:
        print("❌ Main page failed")
        results.append(("Main Page", "FAIL"))
    
    # Test 3: Chat Modes
    print("\n3️⃣ Testing chat modes...")
    modes = ['chat', 'code', 'translate', 'creative', 'math']
    
    for mode in modes:
        test_data = {
            'message': f'Test message for {mode} mode',
            'mode': mode,
            'include_history': False
        }
        
        print(f"   Testing {mode} mode...")
        status, data = test_endpoint(f"{base_url}/chat", 'POST', test_data)
        
        if status == 200 and data and 'response' in data:
            print(f"   ✅ {mode} mode works")
            results.append((f"{mode} mode", "PASS"))
        else:
            print(f"   ❌ {mode} mode failed")
            results.append((f"{mode} mode", "FAIL"))
        
        time.sleep(1)  # Rate limiting
    
    # Test 4: History Management
    print("\n4️⃣ Testing history management...")
    status, data = test_endpoint(f"{base_url}/get_history")
    if status == 200:
        print("✅ History retrieval works")
        results.append(("Get History", "PASS"))
    else:
        print("❌ History retrieval failed")
        results.append(("Get History", "FAIL"))
    
    # Test 5: Clear History
    print("\n5️⃣ Testing clear history...")
    status, data = test_endpoint(f"{base_url}/clear_history", 'POST')
    if status == 200:
        print("✅ Clear history works")
        results.append(("Clear History", "PASS"))
    else:
        print("❌ Clear history failed")
        results.append(("Clear History", "FAIL"))
    
    # Test 6: Get Capabilities
    print("\n6️⃣ Testing capabilities endpoint...")
    status, data = test_endpoint(f"{base_url}/get_capabilities")
    if status == 200 and data and 'capabilities' in data:
        print("✅ Capabilities endpoint works")
        print(f"   Available modes: {', '.join(data['capabilities'].keys())}")
        results.append(("Capabilities", "PASS"))
    else:
        print("❌ Capabilities endpoint failed")
        results.append(("Capabilities", "FAIL"))
    
    # Test 7: Suggestions
    print("\n7️⃣ Testing suggestions...")
    status, data = test_endpoint(f"{base_url}/suggest_prompts?mode=code")
    if status == 200 and data and 'suggestions' in data:
        print("✅ Suggestions work")
        results.append(("Suggestions", "PASS"))
    else:
        print("❌ Suggestions failed")
        results.append(("Suggestions", "FAIL"))
    
    # Test 8: Feedback
    print("\n8️⃣ Testing feedback...")
    feedback_data = {
        'rating': 5,
        'comment': 'Test feedback'
    }
    status, data = test_endpoint(f"{base_url}/feedback", 'POST', feedback_data)
    if status == 200:
        print("✅ Feedback submission works")
        results.append(("Feedback", "PASS"))
    else:
        print("❌ Feedback submission failed")
        results.append(("Feedback", "FAIL"))
    
    # Print Results Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, result in results if result == "PASS")
    failed = sum(1 for _, result in results if result == "FAIL")
    
    for test_name, result in results:
        emoji = "✅" if result == "PASS" else "❌"
        print(f"{emoji} {test_name}: {result}")
    
    print("="*50)
    print(f"Total: {passed} PASSED, {failed} FAILED")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Your Jarvis AI is fully functional!")
    else:
        print(f"\n⚠️ {failed} tests failed. Please check the implementation.")
    
    return passed, failed

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║      JARVIS AI COMPLETE - TEST SUITE    ║
    ╚══════════════════════════════════════════╝
    """)
    
    print("⚠️ Make sure the app is running on localhost:10000")
    print("Start with: python app_complete.py\n")
    
    input("Press Enter to start testing...")
    
    try:
        passed, failed = run_tests()
        
        # Save test report
        with open('test_report.txt', 'w') as f:
            f.write(f"Jarvis AI Test Report\n")
            f.write(f"Date: {datetime.now()}\n")
            f.write(f"Passed: {passed}\n")
            f.write(f"Failed: {failed}\n")
            
        print("\n📄 Test report saved to test_report.txt")
        
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        print("Make sure the app is running!")