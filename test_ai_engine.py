#!/usr/bin/env python
"""
Test Script for Blood Compatibility AI Engine
Verifies all AI functions work correctly
"""

from blood_ai_engine import (
    get_compatible_donors,
    is_donor_compatible,
    filter_compatible_donors,
    get_all_blood_groups,
    get_compatibility_explanation
)

def test_blood_compatibility():
    """Test blood compatibility rules"""
    print("=" * 60)
    print("BLOOD COMPATIBILITY AI ENGINE - TEST SUITE")
    print("=" * 60)
    
    # Test 1: Universal Donor (O-)
    print("\n✓ TEST 1: O- is Universal Donor")
    print("  O- can donate to:")
    compatible = get_compatible_donors('O-')
    print(f"  {compatible}")
    assert compatible == ['O-'], "O- should only receive from O-"
    print("  ✓ PASSED")
    
    # Test 2: Get donors for A+
    print("\n✓ TEST 2: A+ Receiver")
    print("  A+ can receive from:")
    compatible = get_compatible_donors('A+')
    print(f"  {compatible}")
    assert 'O+' in compatible and 'O-' in compatible, "A+ should accept O+, O-"
    assert 'A+' in compatible and 'A-' in compatible, "A+ should accept A+, A-"
    print("  ✓ PASSED")
    
    # Test 3: Universal Recipient (AB+)
    print("\n✓ TEST 3: AB+ is Universal Recipient")
    print("  AB+ can receive from:")
    compatible = get_compatible_donors('AB+')
    print(f"  {compatible}")
    assert len(compatible) == 8, "AB+ should accept all 8 blood groups"
    print("  ✓ PASSED")
    
    # Test 4: is_donor_compatible function
    print("\n✓ TEST 4: Donor Compatibility Check")
    
    # Positive cases
    assert is_donor_compatible('O-', 'A+') == True
    print("  O- can donate to A+: ✓ PASSED")
    
    assert is_donor_compatible('A+', 'AB+') == True
    print("  A+ can donate to AB+: ✓ PASSED")
    
    assert is_donor_compatible('B-', 'B+') == True
    print("  B- can donate to B+: ✓ PASSED")
    
    # Negative cases
    assert is_donor_compatible('AB+', 'O-') == False
    print("  AB+ cannot donate to O-: ✓ PASSED")
    
    assert is_donor_compatible('B+', 'A-') == False
    print("  B+ cannot donate to A-: ✓ PASSED")
    
    # Test 5: Filter compatible donors
    print("\n✓ TEST 5: Filter Compatible Donors")
    
    donors = [
        {'email': 'donor1@test.com', 'name': 'Alice', 'blood_group': 'O-'},
        {'email': 'donor2@test.com', 'name': 'Bob', 'blood_group': 'B+'},
        {'email': 'donor3@test.com', 'name': 'Charlie', 'blood_group': 'A+'},
        {'email': 'donor4@test.com', 'name': 'David', 'blood_group': 'A-'},
    ]
    
    # Filter for A+ receiver
    compatible = filter_compatible_donors(donors, 'A+')
    compatible_names = [d['name'] for d in compatible]
    print(f"  Donors compatible with A+ receiver: {compatible_names}")
    assert len(compatible) == 3, "Should find 3 compatible donors (O-, A+, A-)"
    assert 'Bob' not in compatible_names, "B+ should not be compatible with A+"
    print("  ✓ PASSED")
    
    # Test 6: Get all blood groups
    print("\n✓ TEST 6: Get All Blood Groups")
    blood_groups = get_all_blood_groups()
    print(f"  Supported blood groups: {sorted(blood_groups)}")
    assert len(blood_groups) == 8, "Should support 8 blood groups"
    print("  ✓ PASSED")
    
    # Test 7: Compatibility explanation
    print("\n✓ TEST 7: Compatibility Explanation")
    explanation = get_compatibility_explanation('AB+')
    print(f"  {explanation}")
    assert 'Universal Recipient' in explanation, "Should mention universal recipient"
    print("  ✓ PASSED")
    
    explanation = get_compatibility_explanation('O-')
    print(f"  {explanation}")
    assert 'Universal Donor' in explanation, "Should mention universal donor"
    print("  ✓ PASSED")
    
    # Test 8: Edge cases
    print("\n✓ TEST 8: Edge Cases")
    
    # Invalid blood group
    invalid = get_compatible_donors('XX')
    print(f"  Invalid blood group 'XX': {invalid}")
    assert invalid == [], "Invalid blood group should return empty list"
    print("  ✓ PASSED")
    
    # Empty donor list
    empty_filtered = filter_compatible_donors([], 'A+')
    print(f"  Filter empty donor list: {empty_filtered}")
    assert empty_filtered == [], "Empty list should return empty list"
    print("  ✓ PASSED")
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! AI ENGINE IS WORKING CORRECTLY!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        test_blood_compatibility()
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        exit(1)
