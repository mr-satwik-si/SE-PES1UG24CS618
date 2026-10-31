import pytest

from cloud_storage_tier import (
    process_storage_tenants,
    monitor_replication_latency
)


def test_hot_tier():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{"size_gb": 100, "egress_gb": 50}]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result == {
        "total_billed": 2.5,
        "status": "BILLED"
    }


def test_cool_tier():
    tenants = [{
        "account_active": True,
        "tier": "cool",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["total_billed"] == 1.5


def test_archive_tier():
    tenants = [{
        "account_active": True,
        "tier": "archive",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["total_billed"] == 0.5


def test_inactive_tenant():
    tenants = [{
        "account_active": False,
        "tier": "hot",
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["status"] == "ZERO_USAGE"


def test_invalid_tier():
    tenants = [{
        "account_active": True,
        "tier": "unknown",
        "buckets": []
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["status"] == "ZERO_USAGE"


def test_invalid_bucket_size():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [
            {"size_gb": 0},
            {"size_gb": -10}
        ]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["status"] == "ZERO_USAGE"


def test_corrupted_hot_bucket():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{
            "size_gb": 100,
            "corrupted": True
        }]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["total_billed"] == 0


def test_large_bucket():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{"size_gb": 600}]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["total_billed"] == 13.5


def test_high_egress():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [{
            "size_gb": 100,
            "egress_gb": 150
        }]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["total_billed"] == 6.5


def test_backup_vault():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "has_backup_vault": True,
        "buckets": [{"size_gb": 100}]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["total_billed"] == 12.5


def test_archive_corrupted_bucket():
    tenants = [{
        "account_active": True,
        "tier": "archive",
        "has_backup_vault": False,
        "buckets": [{
            "size_gb": 100,
            "corrupted": True
        }]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["total_billed"] == 0


def test_audit_flagged():
    tenants = [{
        "account_active": True,
        "tier": "hot",
        "buckets": [
            {"size_gb": 0},
            {"size_gb": 0},
            {"size_gb": 0},
            {"size_gb": 0},
            {"size_gb": 0}
        ]
    }]

    result = process_storage_tenants(tenants, 10)

    assert result["status"] == "AUDIT_FLAGGED"


def test_no_cluster_data():
    assert monitor_replication_latency([]) == "NO_DATA"


def test_normal_replication():
    assert monitor_replication_latency([
        [100, 150, 180],
        [90, 120, 160]
    ]) == "SYNCED"


def test_single_high_latency():
    assert monitor_replication_latency([
        [250, 100, 150]
    ]) == "SYNCED"


def test_consecutive_high_latency():
    assert monitor_replication_latency([
        [250, 260]
    ]) == "SYNC_LAG_ALERT"


def test_latency_streak_reset():
    assert monitor_replication_latency([
        [250, 100, 260]
    ]) == "SYNCED"

def test_invalid_tenants_input():
    with pytest.raises(ValueError):
        process_storage_tenants("invalid", 10)


def test_negative_support_fee():
    with pytest.raises(ValueError):
        process_storage_tenants([], -1)