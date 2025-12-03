"""
Data gathering tools for the investigation agent.

These are mock implementations that simulate API calls and database lookups.
In a production environment, these would be replaced with actual integrations.
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import random


def seed_random(entity_id: str):
    """
    Seed the random number generator based on entity_id for deterministic results.
    This ensures the same entity always gets the same mock data.
    """
    # Convert entity_id to a consistent integer seed
    seed_value = sum(ord(c) for c in entity_id)
    random.seed(seed_value)


def fetch_user_profile(entity_id: str) -> Dict[str, Any]:
    """
    Fetch user profile information.
    
    Args:
        entity_id: The user ID to look up
        
    Returns:
        User profile data including account details and verification status
    """
    # Demo entities with hardcoded profiles
    if entity_id == "USER_001":  # Low-risk profile
        return {
            "user_id": entity_id,
            "username": f"user_{entity_id}",
            "email": f"{entity_id}@example.com",
            "registration_date": (datetime.now() - timedelta(days=500)).isoformat(),
            "account_age_days": 500,
            "verification_status": "verified",
            "country": "US",
            "account_status": "active",
            "kyc_completed": True
        }
    elif entity_id == "USER_002":  # Medium-risk profile
        return {
            "user_id": entity_id,
            "username": f"user_{entity_id}",
            "email": f"{entity_id}@example.com",
            "registration_date": (datetime.now() - timedelta(days=120)).isoformat(),
            "account_age_days": 120,
            "verification_status": "pending",
            "country": "VN",
            "account_status": "active",
            "kyc_completed": False
        }
    elif entity_id == "USER_003":  # High-risk profile
        return {
            "user_id": entity_id,
            "username": f"user_{entity_id}",
            "email": f"{entity_id}@example.com",
            "registration_date": (datetime.now() - timedelta(days=15)).isoformat(),
            "account_age_days": 15,
            "verification_status": "unverified",
            "country": "Unknown",
            "account_status": "active",
            "kyc_completed": False
        }
    
    # Seed random for deterministic results
    seed_random(entity_id)
    
    # Mock data - replace with actual API call
    registration_days_ago = random.randint(30, 730)
    registration_date = datetime.now() - timedelta(days=registration_days_ago)
    
    return {
        "user_id": entity_id,
        "username": f"user_{entity_id}",
        "email": f"{entity_id}@example.com",
        "registration_date": registration_date.isoformat(),
        "account_age_days": registration_days_ago,
        "verification_status": random.choice(["verified", "unverified", "pending"]),
        "country": random.choice(["US", "UK", "CA", "DE", "SG", "VN", "PH"]),
        "account_status": "active",
        "kyc_completed": random.choice([True, False])
    }


def fetch_activity_logs(entity_id: str) -> Dict[str, Any]:
    """
    Fetch recent activity logs for the user.
    
    Args:
        entity_id: The user ID to look up
        
    Returns:
        Activity data including logins, transactions, and device information
    """
    # Seed random for deterministic results
    seed_random(entity_id)
    
    # Mock data - simulate various activity patterns
    num_logins = random.randint(5, 50)
    num_transactions = random.randint(0, 100)
    
    # Generate login history
    logins = []
    for i in range(min(num_logins, 10)):  # Last 10 logins
        login_time = datetime.now() - timedelta(hours=random.randint(1, 720))
        logins.append({
            "timestamp": login_time.isoformat(),
            "ip_address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "device": random.choice(["iPhone", "Android", "Desktop", "iPad"]),
            "location": random.choice(["New York, US", "London, UK", "Singapore, SG", "Ho Chi Minh, VN", "Unknown"])
        })
    
    return {
        "total_logins": num_logins,
        "total_transactions": num_transactions,
        "recent_logins": logins,
        "vpn_usage_detected": random.choice([True, False]),
        "multiple_devices": len(set(login["device"] for login in logins)) > 2,
        "geographic_spread": len(set(login["location"] for login in logins))
    }


def fetch_connected_accounts(entity_id: str) -> Dict[str, Any]:
    """
    Fetch connected accounts and social graph.
    
    Args:
        entity_id: The user ID to look up
        
    Returns:
        Connected accounts and relationship data
    """
    # Seed random for deterministic results
    seed_random(entity_id)
    
    num_connections = random.randint(0, 20)
    
    connections = []
    for i in range(min(num_connections, 5)):  # Show up to 5 connections
        connections.append({
            "account_id": f"ACC_{random.randint(1000, 9999)}",
            "relationship": random.choice(["linked_email", "shared_device", "shared_ip", "transaction_partner"]),
            "confidence": random.uniform(0.5, 1.0)
        })
    
    return {
        "total_connections": num_connections,
        "linked_accounts": connections,
        "follows": random.randint(0, 1000),
        "followers": random.randint(0, 1000),
        "mutual_follows": random.randint(0, 100)
    }


def fetch_past_flags(entity_id: str) -> Dict[str, Any]:
    """
    Fetch past flags and investigation history.
    
    Args:
        entity_id: The user ID to look up
        
    Returns:
        Historical alert and investigation data
    """
    # Seed random for deterministic results
    seed_random(entity_id)
    
    # Demo entities with hardcoded flags
    if entity_id == "USER_001":  # Low-risk: minimal flags
        return {
            "total_flags": 0,
            "past_flags": [],
            "cleared_flags": 0,
            "active_investigations": 0
        }
    elif entity_id == "USER_002":  # Medium-risk: some cleared flags
        return {
            "total_flags": 2,
            "past_flags": [
                {
                    "flag_id": "FLAG_12345",
                    "timestamp": (datetime.now() - timedelta(days=90)).isoformat(),
                    "flag_type": "geographic_anomaly",
                    "resolution": "cleared",
                    "severity": "low"
                },
                {
                    "flag_id": "FLAG_12346",
                    "timestamp": (datetime.now() - timedelta(days=30)).isoformat(),
                    "flag_type": "rapid_follow_unfollow",
                    "resolution": "warning_issued",
                    "severity": "medium"
                }
            ],
            "cleared_flags": 1,
            "active_investigations": 0
        }
    elif entity_id == "USER_003":  # High-risk: multiple serious flags
        return {
            "total_flags": 4,
            "past_flags": [
                {
                    "flag_id": "FLAG_99001",
                    "timestamp": (datetime.now() - timedelta(days=5)).isoformat(),
                    "flag_type": "multiple_account_coordination",
                    "resolution": "under_review",
                    "severity": "high"
                },
                {
                    "flag_id": "FLAG_99002",
                    "timestamp": (datetime.now() - timedelta(days=10)).isoformat(),
                    "flag_type": "high_value_cash_out",
                    "resolution": "temporary_ban",
                    "severity": "high"
                },
                {
                    "flag_id": "FLAG_99003",
                    "timestamp": (datetime.now() - timedelta(days=12)).isoformat(),
                    "flag_type": "suspicious_transaction_pattern",
                    "resolution": "under_review",
                    "severity": "high"
                },
                {
                    "flag_id": "FLAG_99004",
                    "timestamp": (datetime.now() - timedelta(days=14)).isoformat(),
                    "flag_type": "geographic_anomaly",
                    "resolution": "warning_issued",
                    "severity": "medium"
                }
            ],
            "cleared_flags": 0,
            "active_investigations": 2
        }
    
    num_flags = random.randint(0, 5)
    
    flags = []
    for i in range(num_flags):
        flag_time = datetime.now() - timedelta(days=random.randint(1, 365))
        flags.append({
            "flag_id": f"FLAG_{random.randint(10000, 99999)}",
            "timestamp": flag_time.isoformat(),
            "flag_type": random.choice([
                "suspicious_transaction_pattern",
                "rapid_follow_unfollow",
                "geographic_anomaly",
                "high_value_cash_out",
                "multiple_account_coordination"
            ]),
            "resolution": random.choice(["cleared", "warning_issued", "temporary_ban", "under_review"]),
            "severity": random.choice(["low", "medium", "high"])
        })
    
    return {
        "total_flags": num_flags,
        "past_flags": flags,
        "cleared_flags": sum(1 for f in flags if f["resolution"] == "cleared"),
        "active_investigations": sum(1 for f in flags if f["resolution"] == "under_review")
    }


def fetch_transactions(entity_id: str) -> Dict[str, Any]:
    """
    Fetch transaction history.
    
    Args:
        entity_id: The user ID to look up
        
    Returns:
        Transaction data with amounts, recipients, and patterns
    """
    # Seed random for deterministic results
    seed_random(entity_id)
    
    # Demo entities with hardcoded transactions
    if entity_id == "USER_001":  # Low-risk: normal activity
        transactions = [
            {"transaction_id": "TXN_100001", "timestamp": (datetime.now() - timedelta(hours=48)).isoformat(), "amount": 50.00, "currency": "USD", "type": "purchase", "recipient": "USER_5001", "status": "completed"},
            {"transaction_id": "TXN_100002", "timestamp": (datetime.now() - timedelta(hours=72)).isoformat(), "amount": 25.00, "currency": "USD", "type": "gift_sent", "recipient": "USER_5002", "status": "completed"},
            {"transaction_id": "TXN_100003", "timestamp": (datetime.now() - timedelta(hours=120)).isoformat(), "amount": 100.00, "currency": "USD", "type": "deposit", "recipient": "SYSTEM", "status": "completed"},
        ]
        return {
            "total_transactions": 15,
            "recent_transactions": transactions,
            "total_volume_usd": 450.00,
            "last_24h_transactions": 0,
            "last_24h_volume_usd": 0.00,
            "avg_transaction_size": 30.00,
            "cash_out_ratio": 0.0
        }
    elif entity_id == "USER_002":  # Medium-risk: moderate suspicious activity
        transactions = [
            {"transaction_id": "TXN_200001", "timestamp": (datetime.now() - timedelta(hours=12)).isoformat(), "amount": 500.00, "currency": "USD", "type": "cash_out", "recipient": "EXTERNAL", "status": "completed"},
            {"transaction_id": "TXN_200002", "timestamp": (datetime.now() - timedelta(hours=18)).isoformat(), "amount": 200.00, "currency": "USD", "type": "gift_sent", "recipient": "USER_6001", "status": "completed"},
            {"transaction_id": "TXN_200003", "timestamp": (datetime.now() - timedelta(hours=20)).isoformat(), "amount": 180.00, "currency": "USD", "type": "gift_received", "recipient": "USER_6001", "status": "completed"},
            {"transaction_id": "TXN_200004", "timestamp": (datetime.now() - timedelta(hours=24)).isoformat(), "amount": 300.00, "currency": "USD", "type": "purchase", "recipient": "USER_6002", "status": "completed"},
        ]
        return {
            "total_transactions": 35,
            "recent_transactions": transactions,
            "total_volume_usd": 2500.00,
            "last_24h_transactions": 4,
            "last_24h_volume_usd": 1180.00,
            "avg_transaction_size": 71.43,
            "cash_out_ratio": 0.15
        }
    elif entity_id == "USER_003":  # High-risk: very suspicious activity
        transactions = [
            {"transaction_id": "TXN_300001", "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(), "amount": 5000.00, "currency": "USD", "type": "cash_out", "recipient": "EXTERNAL", "status": "flagged"},
            {"transaction_id": "TXN_300002", "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(), "amount": 3500.00, "currency": "USD", "type": "cash_out", "recipient": "EXTERNAL", "status": "completed"},
            {"transaction_id": "TXN_300003", "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(), "amount": 1000.00, "currency": "USD", "type": "gift_sent", "recipient": "USER_7001", "status": "completed"},
            {"transaction_id": "TXN_300004", "timestamp": (datetime.now() - timedelta(hours=7)).isoformat(), "amount": 950.00, "currency": "USD", "type": "gift_received", "recipient": "USER_7001", "status": "completed"},
            {"transaction_id": "TXN_300005", "timestamp": (datetime.now() - timedelta(hours=8)).isoformat(), "amount": 1000.00, "currency": "USD", "type": "gift_sent", "recipient": "USER_7002", "status": "completed"},
            {"transaction_id": "TXN_300006", "timestamp": (datetime.now() - timedelta(hours=9)).isoformat(), "amount": 980.00, "currency": "USD", "type": "gift_received", "recipient": "USER_7002", "status": "completed"},
        ]
        return {
            "total_transactions": 50,
            "recent_transactions": transactions,
            "total_volume_usd": 15000.00,
            "last_24h_transactions": 6,
            "last_24h_volume_usd": 12430.00,
            "avg_transaction_size": 300.00,
            "cash_out_ratio": 0.45
        }
    
    num_transactions = random.randint(10, 100)
    
    # Generate recent transactions
    transactions = []
    total_volume = 0
    
    for i in range(min(num_transactions, 20)):  # Last 20 transactions
        amount = random.uniform(10, 5000)
        total_volume += amount
        trans_time = datetime.now() - timedelta(hours=random.randint(1, 720))
        
        transactions.append({
            "transaction_id": f"TXN_{random.randint(100000, 999999)}",
            "timestamp": trans_time.isoformat(),
            "amount": round(amount, 2),
            "currency": "USD",
            "type": random.choice(["gift_sent", "gift_received", "purchase", "cash_out", "deposit"]),
            "recipient": f"USER_{random.randint(1000, 9999)}",
            "status": random.choice(["completed", "pending", "flagged"])
        })
    
    # Calculate velocity metrics
    last_24h_transactions = [t for t in transactions if 
                             datetime.fromisoformat(t["timestamp"]) > datetime.now() - timedelta(hours=24)]
    last_24h_volume = sum(t["amount"] for t in last_24h_transactions)
    
    return {
        "total_transactions": num_transactions,
        "recent_transactions": transactions,
        "total_volume_usd": round(total_volume, 2),
        "last_24h_transactions": len(last_24h_transactions),
        "last_24h_volume_usd": round(last_24h_volume, 2),
        "avg_transaction_size": round(total_volume / num_transactions, 2) if num_transactions > 0 else 0,
        "cash_out_ratio": sum(1 for t in transactions if t["type"] == "cash_out") / len(transactions) if transactions else 0
    }


def gather_all_data(entity_id: str, entity_type: str) -> Dict[str, Any]:
    """
    Gather all data for an entity.
    
    Args:
        entity_id: The entity ID to investigate
        entity_type: Type of entity (user/transaction/account)
        
    Returns:
        Comprehensive data package from all sources
    """
    if entity_type == "user":
        return {
            "profile": fetch_user_profile(entity_id),
            "activity": fetch_activity_logs(entity_id),
            "connections": fetch_connected_accounts(entity_id),
            "flags": fetch_past_flags(entity_id),
            "transactions": fetch_transactions(entity_id),
            "data_sources": ["user_db", "activity_logs", "social_graph", "flag_history", "transaction_db"],
            "query_timestamp": datetime.now().isoformat()
        }
    else:
        # For other entity types, return basic mock data
        return {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "data": "Mock data for non-user entities",
            "query_timestamp": datetime.now().isoformat()
        }
