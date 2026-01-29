"""
Blood Compatibility AI Engine
==============================

A rule-based expert system (AI module) that determines medically compatible
donor blood groups based on a requested blood group.

BLOOD COMPATIBILITY RULES:
- O- (Universal Donor): Can donate to all blood groups
- O+: Can donate to O+, A+, B+, AB+
- A-: Can donate to A-, A+, AB-, AB+
- A+: Can donate to A+, AB+
- B-: Can donate to B-, B+, AB-, AB+
- B+: Can donate to B+, AB+
- AB-: Can donate to AB-, AB+
- AB+ (Universal Recipient): Can only receive from AB+

From a RECEIVER perspective (Requested blood group):
- A+ Receiver: Compatible donors are A+, A-, O+, O-
- O- Receiver: Compatible donors are O-
- AB+ Receiver: Compatible donors are all groups (AB+, AB-, A+, A-, B+, B-, O+, O-)
- B+ Receiver: Compatible donors are B+, B-, O+, O-
- And so on...

This module provides a reusable function to:
1. Take a requested blood group as input
2. Return a list of compatible donor blood groups
"""

# Blood compatibility mapping
# Key: Requested Blood Group (Receiver)
# Value: List of compatible donor blood groups (that can donate to this receiver)

BLOOD_COMPATIBILITY_MAP = {
    'A+': ['A+', 'A-', 'O+', 'O-'],
    'A-': ['A-', 'O-'],
    'B+': ['B+', 'B-', 'O+', 'O-'],
    'B-': ['B-', 'O-'],
    'AB+': ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-'],  # Universal Recipient
    'AB-': ['AB-', 'A-', 'B-', 'O-'],
    'O+': ['O+', 'O-'],
    'O-': ['O-'],  # Universal Donor
}


def get_compatible_donors(requested_blood_group):
    """
    Determine compatible donor blood groups for a requested blood group.
    
    AI LOGIC:
    - This function uses a rule-based expert system (lookup table) to determine
      which blood groups can donate to the requested blood group.
    - The compatibility rules are based on international medical standards for
      blood transfusion safety.
    
    Args:
        requested_blood_group (str): The blood group that needs blood (receiver)
                                      Example: 'A+', 'O-', 'AB+', etc.
    
    Returns:
        list: A list of compatible donor blood groups, or empty list if invalid input
        
    Example:
        >>> get_compatible_donors('A+')
        ['A+', 'A-', 'O+', 'O-']
        
        >>> get_compatible_donors('O-')
        ['O-']
        
        >>> get_compatible_donors('AB+')
        ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-']
    """
    # Validate input and retrieve compatible blood groups
    return BLOOD_COMPATIBILITY_MAP.get(requested_blood_group, [])


def is_donor_compatible(donor_blood_group, requested_blood_group):
    """
    Check if a specific donor's blood group is compatible with a requested blood group.
    
    Args:
        donor_blood_group (str): The blood group of the donor
        requested_blood_group (str): The blood group that needs blood (receiver)
    
    Returns:
        bool: True if compatible, False otherwise
        
    Example:
        >>> is_donor_compatible('O-', 'A+')
        True
        
        >>> is_donor_compatible('B+', 'A+')
        False
    """
    compatible_groups = get_compatible_donors(requested_blood_group)
    return donor_blood_group in compatible_groups


def filter_compatible_donors(donor_list, requested_blood_group):
    """
    Filter a list of donors to show only those with compatible blood groups.
    
    AI FILTERING LOGIC:
    - Takes a list of donor objects/dicts and filters them based on blood compatibility
    - Returns only donors whose blood group matches the compatibility rules for
      the requested blood group
    
    Args:
        donor_list (list): List of donor dictionaries, each with at least a 'blood_group' key
        requested_blood_group (str): The blood group that needs blood (receiver)
    
    Returns:
        list: Filtered list of compatible donors
        
    Example:
        donors = [
            {'email': 'donor1@example.com', 'blood_group': 'O-', ...},
            {'email': 'donor2@example.com', 'blood_group': 'B+', ...},
            {'email': 'donor3@example.com', 'blood_group': 'A+', ...}
        ]
        
        compatible = filter_compatible_donors(donors, 'A+')
        # Returns [donor1, donor3] (O- and A+ are compatible with A+ receiver)
    """
    compatible_groups = get_compatible_donors(requested_blood_group)
    return [
        donor for donor in donor_list
        if donor.get('blood_group') in compatible_groups
    ]


def get_all_blood_groups():
    """
    Get a list of all valid blood groups.
    
    Returns:
        list: All blood groups supported by the system
    """
    return list(BLOOD_COMPATIBILITY_MAP.keys())


def get_compatibility_explanation(requested_blood_group):
    """
    Get a human-readable explanation of blood group compatibility.
    
    Args:
        requested_blood_group (str): The blood group to explain
    
    Returns:
        str: A detailed explanation of which blood groups can donate
        
    Example:
        >>> get_compatibility_explanation('AB+')
        'AB+ Blood Group: Can receive from all blood groups (Universal Recipient). 
         Compatible donors: AB+, AB-, A+, A-, B+, B-, O+, O-'
    """
    compatible = get_compatible_donors(requested_blood_group)
    
    if not compatible:
        return f"Unknown blood group: {requested_blood_group}"
    
    # Add special labels for universal donor/recipient
    special_labels = ""
    if requested_blood_group == 'AB+':
        special_labels = " (Universal Recipient)"
    elif requested_blood_group == 'O-':
        special_labels = " (Universal Donor)"
    
    compatible_str = ', '.join(compatible)
    return (f"{requested_blood_group}{special_labels} Blood Group: "
            f"Compatible donors are: {compatible_str}")
