# Decision Path Analysis

Generated from: `food_safety.txt`  
Date: 2025-03-22 13:05:08

## Decision Path Tree

```
└── Do you have a food thermometer available for temperature checks?
└── Yes
    └── Is the food stored at the proper temperature (below 40°F for refrigerated items, below 0°F for frozen items)?
    └── Not sure
        └── Can you check the temperature with a food thermometer?
        └── Yes, and it's not at proper temperature
            └── RESULT: The food is UNSAFE. Foods kept at improper temperatures allow bacteria to multiply rapidly. According to food safety guidelines, perishable foods should not be in the "danger zone" (40°F-140°F) for more than 2 hours.
```

## Visual Diagram

```mermaid
graph TD
    node_Q0["Do you have a food thermometer available for temperature checks?"]
    node_Q1["Is the food stored at the proper temperature (below 40°F for refrigerated items, below 0°F for frozen items)?"]
    node_Q1a["Can you check the temperature with a food thermometer?"]
    node_R1["RESULT: The food is UNSAFE. Foods kept at improper temperatures allow bacteria to multiply rapidly. According to food safety guidelines, perishable foods should not be in the 'danger zone' (40°F-140°F) for more than 2 hours."]
    node_Q0 -->|"Yes"| node_Q1
    node_Q1 -->|"Not sure"| node_Q1a
    node_Q1a -->|"Yes, and it's not at proper temperature"| node_R1

    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef current fill:#d4f4ff,stroke:#0077b6,stroke-width:2px;
    classDef result fill:#d8f3dc,stroke:#2d6a4f,stroke-width:2px;
    class node_Q0,node_Q1,node_Q1a,node_R1 current;
    class node_R1 result;
```
