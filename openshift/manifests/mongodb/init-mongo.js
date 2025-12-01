// MongoDB initialization script
// This script runs automatically when MongoDB container starts for the first time
// It creates sample IT operations data for use with the MongoDB MCP server

// Switch to the target database
db = db.getSiblingDB('mcp_demo');

// Clear existing collections (in case of re-initialization)
db.incidents.drop();
db.services.drop();
db.alerts.drop();

print("✅ Cleared existing collections");

// Insert sample incidents
db.incidents.insertMany([
  {
    id: "INC-001",
    title: "Web server high CPU usage",
    status: "resolved",
    priority: "high",
    created: new Date("2024-11-25T10:00:00Z"),
    resolved: new Date("2024-11-25T11:30:00Z"),
    description: "Web server CPU usage spiked to 95% causing slow response times",
    resolution: "Restarted web server and cleared cache",
    affected_services: ["web-server", "nginx"]
  },
  {
    id: "INC-002",
    title: "Database connection timeout",
    status: "open",
    priority: "critical",
    created: new Date("2024-11-27T14:20:00Z"),
    description: "Application unable to connect to database. Connection timeout errors.",
    affected_services: ["database", "postgresql"]
  },
  {
    id: "INC-003",
    title: "Disk space warning",
    status: "resolved",
    priority: "medium",
    created: new Date("2024-11-26T08:15:00Z"),
    resolved: new Date("2024-11-26T09:00:00Z"),
    description: "Disk usage reached 85% on /var/log partition",
    resolution: "Cleaned old log files and rotated logs",
    affected_services: ["logging"]
  },
  {
    id: "INC-004",
    title: "Cache service degraded performance",
    status: "open",
    priority: "medium",
    created: new Date("2024-11-27T16:45:00Z"),
    description: "Cache service showing degraded performance with high memory usage",
    affected_services: ["cache-service", "redis"]
  },
  {
    id: "INC-005",
    title: "API endpoint returning 500 errors",
    status: "resolved",
    priority: "high",
    created: new Date("2024-11-24T12:00:00Z"),
    resolved: new Date("2024-11-24T13:15:00Z"),
    description: "API endpoint /api/v1/users returning 500 errors for 15 minutes",
    resolution: "Fixed bug in user authentication service",
    affected_services: ["api-server", "auth-service"]
  }
]);

print("✅ Inserted " + db.incidents.countDocuments() + " incidents");

// Insert sample services
db.services.insertMany([
  {
    name: "web-server",
    type: "application",
    status: "online",
    cpu_usage: 45,
    memory_usage: 60,
    last_updated: new Date(),
    endpoints: ["http://web.example.com", "https://web.example.com"],
    dependencies: ["database", "cache-service"]
  },
  {
    name: "database",
    type: "database",
    status: "online",
    cpu_usage: 30,
    memory_usage: 50,
    last_updated: new Date(),
    version: "PostgreSQL 14.5",
    connections: 45,
    max_connections: 100
  },
  {
    name: "cache-service",
    type: "cache",
    status: "degraded",
    cpu_usage: 85,
    memory_usage: 90,
    last_updated: new Date(),
    version: "Redis 7.0",
    hit_rate: 0.72
  },
  {
    name: "api-server",
    type: "application",
    status: "online",
    cpu_usage: 25,
    memory_usage: 40,
    last_updated: new Date(),
    endpoints: ["http://api.example.com/v1"],
    requests_per_second: 150
  },
  {
    name: "logging",
    type: "infrastructure",
    status: "online",
    cpu_usage: 15,
    memory_usage: 35,
    last_updated: new Date(),
    log_volume_gb: 12.5
  }
]);

print("✅ Inserted " + db.services.countDocuments() + " services");

// Insert sample alerts
db.alerts.insertMany([
  {
    id: "ALT-001",
    severity: "high",
    status: "resolved",
    service: "web-server",
    message: "CPU usage exceeded 90% threshold",
    created: new Date("2024-11-25T10:05:00Z"),
    resolved: new Date("2024-11-25T11:30:00Z"),
    metric: "cpu_usage",
    value: 95
  },
  {
    id: "ALT-002",
    severity: "critical",
    status: "open",
    service: "database",
    message: "Database connection failures detected",
    created: new Date("2024-11-27T14:20:00Z"),
    metric: "connection_errors",
    value: 150
  },
  {
    id: "ALT-003",
    severity: "medium",
    status: "resolved",
    service: "logging",
    message: "Disk usage exceeded 80% threshold",
    created: new Date("2024-11-26T08:20:00Z"),
    resolved: new Date("2024-11-26T09:00:00Z"),
    metric: "disk_usage_percent",
    value: 85
  },
  {
    id: "ALT-004",
    severity: "medium",
    status: "open",
    service: "cache-service",
    message: "Memory usage exceeded 85% threshold",
    created: new Date("2024-11-27T16:50:00Z"),
    metric: "memory_usage_percent",
    value: 90
  },
  {
    id: "ALT-005",
    severity: "high",
    status: "resolved",
    service: "api-server",
    message: "Error rate exceeded 5% threshold",
    created: new Date("2024-11-24T12:05:00Z"),
    resolved: new Date("2024-11-24T13:15:00Z"),
    metric: "error_rate_percent",
    value: 12
  }
]);

print("✅ Inserted " + db.alerts.countDocuments() + " alerts");

// Create indexes for better query performance
db.incidents.createIndex({ id: 1 }, { unique: true });
db.incidents.createIndex({ status: 1 });
db.incidents.createIndex({ priority: 1 });
db.incidents.createIndex({ created: -1 });

db.services.createIndex({ name: 1 }, { unique: true });
db.services.createIndex({ status: 1 });
db.services.createIndex({ type: 1 });

db.alerts.createIndex({ id: 1 }, { unique: true });
db.alerts.createIndex({ status: 1 });
db.alerts.createIndex({ severity: 1 });
db.alerts.createIndex({ service: 1 });
db.alerts.createIndex({ created: -1 });

print("✅ Created indexes");

// Show summary
print("\n📊 Database Summary:");
print("   Database: mcp_demo");
print("   Collections:");
print("     - incidents: " + db.incidents.countDocuments());
print("     - services: " + db.services.countDocuments());
print("     - alerts: " + db.alerts.countDocuments());
print("\n✅ Sample data initialization complete!");

