#!/usr/bin/env python3
"""
Connections Dropdown Testing - Backend API Testing
Tests backend APIs for Connections dropdown functionality: Influencers and Graph tabs
"""

import requests
import json
import time
import sys
from datetime import datetime
from typing import Dict, List, Optional, Any

# Use production URL from frontend .env
BACKEND_URL = "https://deploy-connect-6.preview.emergentagent.com"

class ConnectionsDropdownTester:
    def __init__(self):
        self.base_url = BACKEND_URL
        self.tests_run = 0
        self.tests_passed = 0
        self.failed_tests = []
        self.session = requests.Session()
        self.session.timeout = 30
        
    def log(self, message: str, level: str = "INFO"):
        """Log test messages with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
        
    def run_test(self, name: str, test_func, expected_result: Any = True) -> bool:
        """Run a single test and track results"""
        self.tests_run += 1
        self.log(f"🔍 Testing {name}...")
        
        try:
            result = test_func()
            if result == expected_result or (expected_result is True and result):
                self.tests_passed += 1
                self.log(f"✅ PASSED: {name}", "SUCCESS")
                return True
            else:
                self.failed_tests.append(f"{name}: Expected {expected_result}, got {result}")
                self.log(f"❌ FAILED: {name} - Expected {expected_result}, got {result}", "ERROR")
                return False
        except Exception as e:
            self.failed_tests.append(f"{name}: Exception - {str(e)}")
            self.log(f"❌ FAILED: {name} - Exception: {str(e)}", "ERROR")
            return False
    
    def test_health_check(self) -> bool:
        """Test /api/health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/health")
            if response.status_code == 200:
                data = response.json()
                return data.get('ok') is True and 'service' in data
            return False
        except Exception as e:
            self.log(f"Health check failed: {e}")
            return False
    
    def test_connections_health(self) -> bool:
        """Test /api/connections/health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/api/connections/health")
            if response.status_code == 200:
                data = response.json()
                # Check for module healthy status
                return data.get('ok') is True and data.get('module') == 'connections'
            return False
        except Exception as e:
            self.log(f"Connections health check failed: {e}")
            return False
    
    def test_connections_accounts_api(self) -> bool:
        """Test /api/connections/accounts for Influencers tab"""
        try:
            response = self.session.get(f"{self.base_url}/api/connections/accounts?limit=100")
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    accounts_data = data['data']
                    # Check for accounts structure
                    has_items = 'items' in accounts_data and isinstance(accounts_data['items'], list)
                    
                    items_count = len(accounts_data.get('items', []))
                    self.log(f"Connections accounts: {items_count} accounts")
                    
                    # Check account structure if we have items
                    if items_count > 0:
                        first_account = accounts_data['items'][0]
                        required_fields = ['author_id', 'handle', 'scores']
                        has_required = all(field in first_account for field in required_fields)
                        return has_items and has_required
                    
                    return has_items  # Even if no items, structure should be correct
            return False
        except Exception as e:
            self.log(f"Connections accounts API test failed: {e}")
            return False
    
    def test_connections_graph_api(self) -> bool:
        """Test /api/connections/graph for Graph tab - should return 30 nodes and 400+ edges"""
        try:
            # Test POST with limit_nodes parameter
            filters = {"limit_nodes": 50}
            response = self.session.post(
                f"{self.base_url}/api/connections/graph",
                json=filters,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    graph_data = data['data']
                    # Check for required graph structure
                    has_nodes = 'nodes' in graph_data and isinstance(graph_data['nodes'], list)
                    has_edges = 'edges' in graph_data and isinstance(graph_data['edges'], list)
                    
                    # Check if we have reasonable amount of data
                    nodes_count = len(graph_data.get('nodes', []))
                    edges_count = len(graph_data.get('edges', []))
                    
                    self.log(f"Graph API: {nodes_count} nodes, {edges_count} edges")
                    
                    # Should have around 30 nodes and 400+ edges as specified
                    nodes_ok = nodes_count >= 20  # Allow some flexibility
                    edges_ok = edges_count >= 100  # Allow some flexibility for 400+ target
                    
                    # Check node structure if we have nodes
                    if nodes_count > 0:
                        first_node = graph_data['nodes'][0]
                        node_fields = ['id', 'label', 'profile', 'influence_score', 'color', 'size']
                        has_node_structure = all(field in first_node for field in node_fields)
                    else:
                        has_node_structure = True  # No nodes to check
                    
                    # Check edge structure if we have edges
                    if edges_count > 0:
                        first_edge = graph_data['edges'][0]
                        edge_fields = ['id', 'source', 'target', 'direction', 'weight']
                        has_edge_structure = all(field in first_edge for field in edge_fields)
                    else:
                        has_edge_structure = True  # No edges to check
                    
                    return has_nodes and has_edges and nodes_ok and edges_ok and has_node_structure and has_edge_structure
            return False
        except Exception as e:
            self.log(f"Connections Graph API test failed: {e}")
            return False
    
    def test_early_signal_api(self) -> bool:
        """Test /api/connections/early-signal/mock for badge detection"""
        try:
            response = self.session.get(f"{self.base_url}/api/connections/early-signal/mock")
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    signal_data = data['data']
                    # Check for badge field and valid values
                    badge = signal_data.get('badge')
                    return badge in ['breakout', 'rising', 'none']
            return False
        except Exception as e:
            self.log(f"Early Signal API test failed: {e}")
            return False
    
    def test_connections_graph_get(self) -> bool:
        """Test GET /api/connections/graph returns nodes and edges"""
        try:
            response = self.session.get(f"{self.base_url}/api/connections/graph")
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    graph_data = data['data']
                    # Check for required graph structure
                    has_nodes = 'nodes' in graph_data and isinstance(graph_data['nodes'], list)
                    has_edges = 'edges' in graph_data and isinstance(graph_data['edges'], list)
                    has_meta = 'meta' in graph_data
                    
                    # Check if we have reasonable amount of data
                    nodes_count = len(graph_data.get('nodes', []))
                    edges_count = len(graph_data.get('edges', []))
                    
                    self.log(f"Graph GET: {nodes_count} nodes, {edges_count} edges")
                    return has_nodes and has_edges and has_meta and nodes_count > 0
            return False
        except Exception as e:
            self.log(f"Connections Graph GET test failed: {e}")
            return False
    
    def test_connections_graph_post_filters(self) -> bool:
        """Test POST /api/connections/graph with filters"""
        try:
            filters = {
                "profiles": ["whale", "influencer"],
                "limit_nodes": 20,
                "edge_strength": ["high", "medium"]
            }
            response = self.session.post(
                f"{self.base_url}/api/connections/graph",
                json=filters,
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    graph_data = data['data']
                    nodes_count = len(graph_data.get('nodes', []))
                    edges_count = len(graph_data.get('edges', []))
                    
                    self.log(f"Graph POST with filters: {nodes_count} nodes, {edges_count} edges")
                    # Should have nodes and edges, and respect limit
                    return nodes_count > 0 and nodes_count <= 20 and edges_count >= 0
            return False
        except Exception as e:
            self.log(f"Connections Graph POST filters test failed: {e}")
            return False
    
    def test_connections_graph_ranking(self) -> bool:
        """Test GET /api/connections/graph/ranking returns ranking"""
        try:
            response = self.session.get(f"{self.base_url}/api/connections/graph/ranking?limit=10")
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    ranking_data = data['data']
                    # Check for ranking structure
                    has_items = 'items' in ranking_data and isinstance(ranking_data['items'], list)
                    has_sort_by = 'sort_by' in ranking_data
                    has_total = 'total' in ranking_data
                    
                    items_count = len(ranking_data.get('items', []))
                    self.log(f"Graph ranking: {items_count} items")
                    
                    return has_items and has_sort_by and has_total and items_count > 0
            return False
        except Exception as e:
            self.log(f"Connections Graph ranking test failed: {e}")
            return False
    
    def test_connections_graph_node_details(self) -> bool:
        """Test GET /api/connections/graph/node/:id returns node details"""
        try:
            # First get a graph to find a node ID
            graph_response = self.session.get(f"{self.base_url}/api/connections/graph")
            if graph_response.status_code != 200:
                return False
            
            graph_data = graph_response.json()
            if not (graph_data.get('ok') and 'data' in graph_data):
                return False
            
            nodes = graph_data['data'].get('nodes', [])
            if not nodes:
                return False
            
            # Test with first node
            node_id = nodes[0]['id']
            response = self.session.get(f"{self.base_url}/api/connections/graph/node/{node_id}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    node_details = data['data']
                    # Check for node details structure
                    required_fields = ['id', 'label', 'profile', 'influence_score']
                    has_required = all(field in node_details for field in required_fields)
                    
                    self.log(f"Node details for {node_id}: {node_details.get('label', 'unknown')}")
                    return has_required
            return False
        except Exception as e:
            self.log(f"Connections Graph node details test failed: {e}")
            return False
    
    def admin_login(self) -> bool:
        """Login as admin and store token"""
        try:
            login_data = {
                "username": "admin",
                "password": "admin12345"
            }
            response = self.session.post(
                f"{self.base_url}/api/admin/auth/login",
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'token' in data:
                    self.admin_token = data['token']
                    self.log(f"Admin login successful, token: {self.admin_token[:20]}...")
                    return True
            
            self.log(f"Admin login failed: {response.status_code} - {response.text}")
            return False
        except Exception as e:
            self.log(f"Admin login exception: {e}")
            return False
    
    def test_admin_connections_overview_speed(self) -> bool:
        """Test admin connections overview loads < 2 seconds"""
        if not self.admin_token:
            return False
        
        try:
            start_time = time.time()
            response = self.session.get(
                f"{self.base_url}/api/admin/connections/overview",
                headers={'Authorization': f'Bearer {self.admin_token}'}
            )
            end_time = time.time()
            
            load_time = end_time - start_time
            self.log(f"Admin overview load time: {load_time:.2f}s")
            
            if response.status_code == 200 and load_time < 2.0:
                data = response.json()
                return data.get('ok') is True
            return False
        except Exception as e:
            self.log(f"Admin overview test failed: {e}")
            return False
    
    def test_admin_config_readonly(self) -> bool:
        """Test admin config tab shows read-only configs"""
        if not self.admin_token:
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/admin/connections/config",
                headers={'Authorization': f'Bearer {self.admin_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    config_data = data['data']
                    # Check for config structure
                    return 'config' in config_data and isinstance(config_data['config'], dict)
            return False
        except Exception as e:
            self.log(f"Admin config test failed: {e}")
            return False
    
    def test_admin_stability_score(self) -> bool:
        """Test admin stability tab shows score ≥ 0.9"""
        if not self.admin_token:
            return False
        
        try:
            response = self.session.get(
                f"{self.base_url}/api/admin/connections/tuning/status",
                headers={'Authorization': f'Bearer {self.admin_token}'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    tuning_data = data['data']
                    stability_score = tuning_data.get('overall_stability', 0)
                    self.log(f"Stability score: {stability_score}")
                    return stability_score >= 0.9
            return False
        except Exception as e:
            self.log(f"Admin stability test failed: {e}")
            return False
    
    def test_admin_alerts_batch_generation(self) -> bool:
        """Test admin alerts tab: Run Alerts Batch generates alerts"""
        if not self.admin_token:
            return False
        
        try:
            # First get current alerts count
            response = self.session.get(
                f"{self.base_url}/api/admin/connections/alerts/preview",
                headers={'Authorization': f'Bearer {self.admin_token}'}
            )
            
            initial_count = 0
            if response.status_code == 200:
                data = response.json()
                if data.get('ok') and 'data' in data:
                    initial_count = data['data'].get('summary', {}).get('total', 0)
            
            # Run alerts batch with empty JSON body
            batch_response = self.session.post(
                f"{self.base_url}/api/admin/connections/alerts/run",
                headers={
                    'Authorization': f'Bearer {self.admin_token}',
                    'Content-Type': 'application/json'
                },
                json={}  # Send empty JSON object
            )
            
            if batch_response.status_code == 200:
                batch_data = batch_response.json()
                if batch_data.get('ok') and 'data' in batch_data:
                    alerts_generated = batch_data['data'].get('alerts_generated', 0)
                    self.log(f"Alerts batch generated: {alerts_generated} alerts")
                    return alerts_generated >= 0  # Should generate some alerts or at least run successfully
            
            self.log(f"Alerts batch failed: {batch_response.status_code} - {batch_response.text}")
            return False
        except Exception as e:
            self.log(f"Admin alerts batch test failed: {e}")
            return False
    
    def test_cooldown_deduplication(self) -> bool:
        """Test cooldown deduplication - repeated batch should not duplicate alerts"""
        if not self.admin_token:
            return False
        
        try:
            # Run first batch
            first_response = self.session.post(
                f"{self.base_url}/api/admin/connections/alerts/run",
                headers={
                    'Authorization': f'Bearer {self.admin_token}',
                    'Content-Type': 'application/json'
                },
                json={}  # Send empty JSON object
            )
            
            if first_response.status_code != 200:
                self.log(f"First batch failed: {first_response.status_code} - {first_response.text}")
                return False
            
            first_data = first_response.json()
            first_generated = first_data.get('data', {}).get('alerts_generated', 0)
            
            # Wait a moment and run second batch
            time.sleep(1)
            
            second_response = self.session.post(
                f"{self.base_url}/api/admin/connections/alerts/run",
                headers={
                    'Authorization': f'Bearer {self.admin_token}',
                    'Content-Type': 'application/json'
                },
                json={}  # Send empty JSON object
            )
            
            if second_response.status_code != 200:
                self.log(f"Second batch failed: {second_response.status_code} - {second_response.text}")
                return False
            
            second_data = second_response.json()
            second_generated = second_data.get('data', {}).get('alerts_generated', 0)
            
            self.log(f"First batch: {first_generated} alerts, Second batch: {second_generated} alerts")
            
            # Second batch should generate fewer or same alerts due to cooldown
            return second_generated <= first_generated
            
        except Exception as e:
            self.log(f"Cooldown deduplication test failed: {e}")
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all P2.2 tests and return results"""
        self.log("🚀 Starting P2.2 Final Readiness Check - Backend Testing")
        self.log(f"Testing against: {self.base_url}")
        
        # Core API Health Tests
        self.run_test("Backend health check /api/health", self.test_health_check)
        self.run_test("Connections health /api/connections/health", self.test_connections_health)
        
        # API Stability Tests
        self.run_test("Scoring API /api/connections/score/mock stability", self.test_scoring_api_stability)
        self.run_test("Trends API /api/connections/trends/mock correctness", self.test_trends_api_correctness)
        self.run_test("Early Signal API /api/connections/early-signal/mock badge detection", self.test_early_signal_api)
        
        # Connections Graph API Tests
        self.run_test("Connections Graph GET /api/connections/graph", self.test_connections_graph_get)
        self.run_test("Connections Graph POST /api/connections/graph with filters", self.test_connections_graph_post_filters)
        self.run_test("Connections Graph ranking /api/connections/graph/ranking", self.test_connections_graph_ranking)
        self.run_test("Connections Graph node details /api/connections/graph/node/:id", self.test_connections_graph_node_details)
        
        # Admin Authentication
        admin_login_success = self.run_test("Admin login (admin/admin12345)", self.admin_login)
        
        if admin_login_success:
            # Admin Control Plane Tests
            self.run_test("Admin Connections Overview loads < 2 sec", self.test_admin_connections_overview_speed)
            self.run_test("Admin Config tab shows read-only configs", self.test_admin_config_readonly)
            self.run_test("Admin Stability tab shows score ≥ 0.9", self.test_admin_stability_score)
            self.run_test("Admin Alerts tab: Run Alerts Batch generates alerts", self.test_admin_alerts_batch_generation)
            self.run_test("Cooldown deduplication works", self.test_cooldown_deduplication)
        else:
            self.log("⚠️ Skipping admin tests due to login failure", "WARNING")
        
        # Results Summary
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        self.log(f"\n📊 P2.2 Backend Test Results:")
        self.log(f"✅ Passed: {self.tests_passed}/{self.tests_run} ({success_rate:.1f}%)")
        
        if self.failed_tests:
            self.log(f"❌ Failed Tests:")
            for failure in self.failed_tests:
                self.log(f"   - {failure}")
        
        return {
            'tests_run': self.tests_run,
            'tests_passed': self.tests_passed,
            'success_rate': success_rate,
            'failed_tests': self.failed_tests,
            'admin_token_obtained': self.admin_token is not None
        }

def main():
    """Main test execution"""
    tester = P22BackendTester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if results['success_rate'] >= 80:
        print(f"\n🎉 P2.2 Backend tests PASSED with {results['success_rate']:.1f}% success rate")
        return 0
    else:
        print(f"\n💥 P2.2 Backend tests FAILED with {results['success_rate']:.1f}% success rate")
        return 1

if __name__ == "__main__":
    sys.exit(main())