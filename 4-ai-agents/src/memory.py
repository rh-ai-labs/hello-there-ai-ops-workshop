"""
Agent Memory System

This module provides memory capabilities for agents to learn from
past experiences and improve over time.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class ActionMemory:
    """Memory of a single action taken by the agent"""
    timestamp: float
    action_type: str
    action_params: Dict[str, Any]
    result: Dict[str, Any]
    success: bool
    context: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp,
            "action_type": self.action_type,
            "action_params": self.action_params,
            "result": self.result,
            "success": self.success,
            "context": self.context
        }


@dataclass
class ProblemMemory:
    """Memory of a problem and its solution"""
    problem_description: str
    solution_actions: List[ActionMemory]
    success: bool
    timestamp: float
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "problem_description": self.problem_description,
            "solution_actions": [action.to_dict() for action in self.solution_actions],
            "success": self.success,
            "timestamp": self.timestamp,
            "notes": self.notes
        }


class AgentMemory:
    """
    Memory system for autonomous agents.
    
    Stores past experiences, successful solutions, and learned patterns
    to help agents make better decisions over time.
    """
    
    def __init__(self):
        """Initialize agent memory"""
        self.action_history: List[ActionMemory] = []
        self.problem_solutions: List[ProblemMemory] = []
        self.successful_patterns: Dict[str, List[Dict[str, Any]]] = {}
    
    def remember_action(
        self,
        action_type: str,
        action_params: Dict[str, Any],
        result: Dict[str, Any],
        success: bool,
        context: str = ""
    ):
        """
        Remember an action that was taken.
        
        Args:
            action_type: Type of action (e.g., 'restart_service')
            action_params: Parameters used for the action
            result: Result of the action
            success: Whether the action was successful
            context: Additional context about why the action was taken
        """
        import time
        memory = ActionMemory(
            timestamp=time.time(),
            action_type=action_type,
            action_params=action_params,
            result=result,
            success=success,
            context=context
        )
        self.action_history.append(memory)
    
    def remember_problem_solution(
        self,
        problem_description: str,
        solution_actions: List[ActionMemory],
        success: bool,
        notes: str = ""
    ):
        """
        Remember a problem and its solution.
        
        Args:
            problem_description: Description of the problem
            solution_actions: List of actions taken to solve it
            solution_actions: Actions taken to solve the problem
            success: Whether the problem was solved
            notes: Additional notes about the solution
        """
        import time
        memory = ProblemMemory(
            problem_description=problem_description,
            solution_actions=solution_actions,
            success=success,
            timestamp=time.time(),
            notes=notes
        )
        self.problem_solutions.append(memory)
    
    def get_similar_problems(self, problem_description: str, limit: int = 5) -> List[ProblemMemory]:
        """
        Find similar problems from memory.
        
        Args:
            problem_description: Description of current problem
            limit: Maximum number of similar problems to return
            
        Returns:
            List of similar problems
        """
        # Simple keyword matching (in production, would use embeddings/semantic search)
        keywords = set(problem_description.lower().split())
        
        scored_problems = []
        for problem in self.problem_solutions:
            problem_keywords = set(problem.problem_description.lower().split())
            similarity = len(keywords & problem_keywords) / max(len(keywords | problem_keywords), 1)
            scored_problems.append((similarity, problem))
        
        # Sort by similarity and return top matches
        scored_problems.sort(reverse=True, key=lambda x: x[0])
        return [problem for _, problem in scored_problems[:limit]]
    
    def get_action_statistics(self, action_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics about actions.
        
        Args:
            action_type: Optional filter by action type
            
        Returns:
            Dictionary with statistics
        """
        actions = self.action_history
        if action_type:
            actions = [a for a in actions if a.action_type == action_type]
        
        if not actions:
            return {
                "total": 0,
                "successful": 0,
                "failed": 0,
                "success_rate": 0.0
            }
        
        successful = sum(1 for a in actions if a.success)
        total = len(actions)
        
        return {
            "total": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": successful / total if total > 0 else 0.0
        }
    
    def get_recent_actions(self, limit: int = 10) -> List[ActionMemory]:
        """
        Get recent actions.
        
        Args:
            limit: Maximum number of actions to return
            
        Returns:
            List of recent actions (most recent first)
        """
        return sorted(self.action_history, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_successful_solutions(self, limit: int = 10) -> List[ProblemMemory]:
        """
        Get successful problem solutions.
        
        Args:
            limit: Maximum number of solutions to return
            
        Returns:
            List of successful solutions
        """
        successful = [p for p in self.problem_solutions if p.success]
        return sorted(successful, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def clear(self):
        """Clear all memory"""
        self.action_history = []
        self.problem_solutions = []
        self.successful_patterns = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary"""
        return {
            "action_history": [a.to_dict() for a in self.action_history],
            "problem_solutions": [p.to_dict() for p in self.problem_solutions],
            "statistics": self.get_action_statistics()
        }
    
    def save(self, filepath: str):
        """Save memory to file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def load(self, filepath: str):
        """Load memory from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Reconstruct action history
        self.action_history = [
            ActionMemory(**action_data)
            for action_data in data.get("action_history", [])
        ]
        
        # Reconstruct problem solutions
        self.problem_solutions = [
            ProblemMemory(
                problem_description=prob_data["problem_description"],
                solution_actions=[
                    ActionMemory(**action_data)
                    for action_data in prob_data["solution_actions"]
                ],
                success=prob_data["success"],
                timestamp=prob_data["timestamp"],
                notes=prob_data.get("notes", "")
            )
            for prob_data in data.get("problem_solutions", [])
        ]

