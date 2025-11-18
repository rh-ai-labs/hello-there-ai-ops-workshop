"""
Simulated IT Environment

This module provides a simulated IT environment for safe agent training
and demonstration. In production, this would connect to real IT systems.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import random
import time


class ServiceStatus(Enum):
    """Service status enumeration"""
    RUNNING = "running"
    STOPPED = "stopped"
    DEGRADED = "degraded"
    FAILED = "failed"


@dataclass
class Service:
    """Represents an IT service"""
    name: str
    status: ServiceStatus = ServiceStatus.RUNNING
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    last_restart: Optional[float] = None
    restart_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert service to dictionary"""
        return {
            "name": self.name,
            "status": self.status.value,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "last_restart": self.last_restart,
            "restart_count": self.restart_count,
        }


class SimulatedEnvironment:
    """
    Simulated IT environment for agent interaction.
    
    This provides a safe way to test agents without affecting real systems.
    """
    
    def __init__(self, initial_services: Optional[List[str]] = None):
        """
        Initialize simulated environment.
        
        Args:
            initial_services: List of service names to create
        """
        self.services: Dict[str, Service] = {}
        self.action_log: List[Dict[str, Any]] = []
        self.time: float = time.time()
        
        # Create initial services
        if initial_services:
            for service_name in initial_services:
                self.services[service_name] = Service(name=service_name)
        else:
            # Default services
            default_services = [
                "web-server",
                "database",
                "cache-service",
                "api-gateway",
                "monitoring-service"
            ]
            for service_name in default_services:
                self.services[service_name] = Service(name=service_name)
    
    def get_service_status(self, service_name: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a service.
        
        Args:
            service_name: Name of the service
            
        Returns:
            Service status dictionary or None if service doesn't exist
        """
        if service_name not in self.services:
            return None
        
        service = self.services[service_name]
        
        # Simulate some variability in metrics
        service.cpu_usage = max(0, min(100, service.cpu_usage + random.uniform(-5, 5)))
        service.memory_usage = max(0, min(100, service.memory_usage + random.uniform(-2, 2)))
        
        return service.to_dict()
    
    def get_all_services(self) -> List[Dict[str, Any]]:
        """Get status of all services"""
        return [service.to_dict() for service in self.services.values()]
    
    def restart_service(self, service_name: str) -> Dict[str, Any]:
        """
        Restart a service.
        
        Args:
            service_name: Name of the service to restart
            
        Returns:
            Result dictionary with success status and message
        """
        if service_name not in self.services:
            result = {
                "success": False,
                "message": f"Service '{service_name}' not found",
                "service_name": service_name
            }
            self._log_action("restart_service", result)
            return result
        
        service = self.services[service_name]
        
        # Simulate restart process
        time.sleep(0.1)  # Simulate restart time
        
        service.status = ServiceStatus.RUNNING
        service.last_restart = time.time()
        service.restart_count += 1
        service.cpu_usage = random.uniform(10, 30)  # Reset to normal after restart
        service.memory_usage = random.uniform(20, 40)
        
        result = {
            "success": True,
            "message": f"Service '{service_name}' restarted successfully",
            "service_name": service_name,
            "status": service.status.value,
            "restart_count": service.restart_count
        }
        self._log_action("restart_service", result)
        return result
    
    def scale_service(self, service_name: str, replicas: int) -> Dict[str, Any]:
        """
        Scale a service (simulated - just updates metrics).
        
        Args:
            service_name: Name of the service
            replicas: Number of replicas (not actually used in simulation)
            
        Returns:
            Result dictionary
        """
        if service_name not in self.services:
            result = {
                "success": False,
                "message": f"Service '{service_name}' not found",
                "service_name": service_name
            }
            self._log_action("scale_service", result)
            return result
        
        service = self.services[service_name]
        
        # Simulate scaling effect on metrics
        if replicas > 1:
            service.cpu_usage = max(0, service.cpu_usage - 10 * (replicas - 1))
            service.memory_usage = max(0, service.memory_usage - 5 * (replicas - 1))
        
        result = {
            "success": True,
            "message": f"Service '{service_name}' scaled to {replicas} replicas",
            "service_name": service_name,
            "replicas": replicas,
            "cpu_usage": service.cpu_usage,
            "memory_usage": service.memory_usage
        }
        self._log_action("scale_service", result)
        return result
    
    def simulate_failure(self, service_name: str) -> Dict[str, Any]:
        """
        Simulate a service failure (for testing purposes).
        
        Args:
            service_name: Name of the service to fail
            
        Returns:
            Result dictionary
        """
        if service_name not in self.services:
            return {
                "success": False,
                "message": f"Service '{service_name}' not found"
            }
        
        service = self.services[service_name]
        service.status = ServiceStatus.FAILED
        service.cpu_usage = 0.0
        service.memory_usage = 0.0
        
        result = {
            "success": True,
            "message": f"Simulated failure for service '{service_name}'",
            "service_name": service_name,
            "status": service.status.value
        }
        self._log_action("simulate_failure", result)
        return result
    
    def simulate_degradation(self, service_name: str) -> Dict[str, Any]:
        """
        Simulate service degradation (high CPU/memory).
        
        Args:
            service_name: Name of the service
            
        Returns:
            Result dictionary
        """
        if service_name not in self.services:
            return {
                "success": False,
                "message": f"Service '{service_name}' not found"
            }
        
        service = self.services[service_name]
        service.status = ServiceStatus.DEGRADED
        service.cpu_usage = random.uniform(85, 95)
        service.memory_usage = random.uniform(80, 90)
        
        result = {
            "success": True,
            "message": f"Simulated degradation for service '{service_name}'",
            "service_name": service_name,
            "status": service.status.value,
            "cpu_usage": service.cpu_usage,
            "memory_usage": service.memory_usage
        }
        self._log_action("simulate_degradation", result)
        return result
    
    def _log_action(self, action_type: str, result: Dict[str, Any]):
        """Log an action for audit purposes"""
        log_entry = {
            "timestamp": time.time(),
            "action": action_type,
            "result": result
        }
        self.action_log.append(log_entry)
    
    def get_action_log(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get action log.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of action log entries
        """
        if limit:
            return self.action_log[-limit:]
        return self.action_log
    
    def reset(self):
        """Reset environment to initial state"""
        for service in self.services.values():
            service.status = ServiceStatus.RUNNING
            service.cpu_usage = random.uniform(10, 30)
            service.memory_usage = random.uniform(20, 40)
            service.restart_count = 0
            service.last_restart = None
        self.action_log = []

