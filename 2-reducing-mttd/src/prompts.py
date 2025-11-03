"""
Prompt templates for incident enrichment tasks.
"""

from typing import Dict


def get_base_enrichment_prompt(incident_data: Dict) -> str:
    """
    Base prompt template for enriching incident information.
    
    Args:
        incident_data: Dictionary with incident fields
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are an IT incident analyst. Your task is to enrich the following incident report with missing or unclear information.

**Incident Details:**
- Number: {incident_data.get('number', 'N/A')}
- Date: {incident_data.get('date', 'N/A')}
- Contact Type: {incident_data.get('contact_type', 'N/A')}
- Short Description: {incident_data.get('short_description', 'N/A')}
- Category: {incident_data.get('category', 'N/A')}
- Subcategory: {incident_data.get('subcategory', 'N/A')}
- Customer: {incident_data.get('customer', 'N/A')}

**Incident Content:**
{incident_data.get('content', 'No content provided')}

**Task:**
Please enrich this incident report by:
1. Providing a clear, detailed description of the problem
2. Identifying the root cause (if apparent from the description)
3. Suggesting potential resolution steps
4. Classifying the priority level (Low, Medium, High, Critical)
5. Recommending the appropriate assignment group

Provide your response in a structured format with clear sections.
"""
    return prompt


def get_structured_enrichment_prompt(incident_data: Dict) -> str:
    """
    Structured prompt that requests JSON output for easier parsing.
    
    Args:
        incident_data: Dictionary with incident fields
        
    Returns:
        Formatted prompt string requesting JSON response
    """
    prompt = f"""You are an IT incident analyst. Analyze the following incident and provide enriched information in JSON format.

**Incident:**
{incident_data.get('content', 'No content provided')}

**Required JSON Structure:**
{{
  "detailed_description": "Clear, detailed description of the problem",
  "root_cause": "Identified or suspected root cause",
  "resolution_steps": ["Step 1", "Step 2", "Step 3"],
  "priority": "Low|Medium|High|Critical",
  "recommended_assignment_group": "Suggested team name",
  "urgency": "Low|Medium|High|Critical",
  "impact_analysis": "Brief analysis of business impact"
}}

Respond ONLY with valid JSON, no additional text.
"""
    return prompt


def get_minimal_enrichment_prompt(incident_data: Dict) -> str:
    """
    Minimal prompt for quick enrichment (Scenario A - general LLM).
    
    Args:
        incident_data: Dictionary with incident fields
        
    Returns:
        Simple prompt string
    """
    prompt = f"""Enrich this IT incident with more details:

{incident_data.get('content', 'No content provided')}

Provide additional context and resolution steps.
"""
    return prompt


def get_detailed_enrichment_prompt(incident_data: Dict) -> str:
    """
    Detailed prompt with specific instructions (Scenario B - tuned LLM).
    
    Args:
        incident_data: Dictionary with incident fields
        
    Returns:
        Detailed prompt with specific guidelines
    """
    prompt = f"""You are an expert IT incident analyst. Analyze the following incident following these guidelines:

**Incident Information:**
- Number: {incident_data.get('number', 'N/A')}
- Date: {incident_data.get('date', 'N/A')}
- Category: {incident_data.get('category', 'N/A')}
- Subcategory: {incident_data.get('subcategory', 'N/A')}

**Incident Description:**
{incident_data.get('content', 'No content provided')}

**Analysis Guidelines:**
1. **Detailed Description**: Expand the incident description with technical specifics, error messages, and user-reported symptoms
2. **Root Cause**: Identify the most likely root cause based on:
   - Error patterns
   - System/application involved
   - User actions before the incident
3. **Resolution Steps**: Provide 3-5 specific, actionable steps in order of execution
4. **Priority Assessment**: Rate priority based on:
   - Business impact (Low/Medium/High/Critical)
   - User count affected
   - Service criticality
5. **Assignment Group**: Recommend the most appropriate team based on:
   - System/application affected ({incident_data.get('software/system', 'Unknown')})
   - Category and subcategory
   - Technical complexity

**Output Format (JSON):**
{{
  "detailed_description": "...",
  "root_cause": "...",
  "resolution_steps": ["...", "..."],
  "priority": "...",
  "urgency": "...",
  "recommended_assignment_group": "...",
  "impact_analysis": "...",
  "estimated_resolution_time_minutes": <number>
}}

Ensure all fields are specific, accurate, and actionable. Avoid vague statements.
"""
    return prompt


def get_prompt_variants() -> Dict[str, callable]:
    """
    Get dictionary of all available prompt variants.
    
    Returns:
        Dictionary mapping prompt names to prompt functions
    """
    return {
        'base': get_base_enrichment_prompt,
        'structured': get_structured_enrichment_prompt,
        'minimal': get_minimal_enrichment_prompt,
        'detailed': get_detailed_enrichment_prompt,
    }

