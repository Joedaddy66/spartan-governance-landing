# Phi-Core: Policy & Compliance Automation

## Overview

Phi-Core is Veritas Stack's policy engine and compliance automation framework, enabling organizations to codify governance policies, automate compliance checks, and maintain audit-ready documentation.

**Named after**: The golden ratio (Φ), representing balance and harmony—essential qualities for effective governance.

---

## Core Capabilities

### 1. Policy as Code

**Codified Governance**

Define policies in human-readable YAML that are automatically enforced:

```yaml
policy:
  id: gdpr-data-access
  version: 1.0
  description: Enforce GDPR data access controls

  rules:
    - name: require_consent
      condition: data_type == "personal_data"
      requires:
        - user_consent.obtained == true
        - user_consent.timestamp < 2_years_ago

    - name: purpose_limitation
      condition: access_purpose NOT IN allowed_purposes
      action: deny

    - name: audit_access
      condition: always
      action: log
      metadata:
        compliance_framework: "GDPR Article 30"
```

**Policy Features**:
- Version control and rollback
- Testing and validation before deployment
- A/B testing of policy changes
- Automatic documentation generation

---

### 2. Compliance Frameworks

**Pre-Built Framework Support**

| Framework | Coverage | Status | Last Updated |
|-----------|----------|--------|--------------|
| **SOC 2 Type II** | 100% | Certified | Q4 2024 |
| **GDPR** | 100% | Compliant | Q4 2024 |
| **HIPAA** | 100% | Compliant | Q4 2024 |
| **PCI DSS v4.0** | 100% | Compliant | Q3 2024 |
| **ISO 27001** | 100% | Certified | Q4 2024 |
| **CCPA** | 100% | Compliant | Q4 2024 |
| **FedRAMP** | 80% | In Progress | Q1 2025 |
| **NIST 800-53** | 90% | In Progress | Q1 2025 |

**Framework Activation**:
```yaml
compliance_frameworks:
  enabled:
    - soc2
    - gdpr
    - hipaa

  gdpr:
    data_protection_officer: dpo@example.com
    data_retention_default: 730d  # 2 years
    right_to_erasure: enabled

  hipaa:
    covered_entity: true
    encryption_required: true
    audit_log_retention: 6y
```

---

### 3. Automated Audit Trails

**Comprehensive Activity Logging**

Every action is logged with:
- Who performed the action
- What resource was accessed
- When it occurred
- Why (business justification)
- Where (IP, location, device)
- How (API, UI, CLI)

**Audit Log Example**:
```json
{
  "audit_id": "aud-2025-11-23-123456",
  "timestamp": "2025-11-23T10:30:45.123Z",
  "actor": {
    "user_id": "user-12345",
    "email": "analyst@company.com",
    "role": "data_analyst",
    "ip_address": "192.168.1.100",
    "location": "San Francisco, CA"
  },
  "action": {
    "type": "data_access",
    "resource": "customer_database.pii_table",
    "operation": "SELECT",
    "query": "SELECT name, email FROM customers WHERE...",
    "rows_affected": 150
  },
  "authorization": {
    "policy_id": "gdpr-data-access",
    "decision": "allow",
    "justification": "Legitimate business purpose",
    "approver": "manager-789"
  },
  "compliance": {
    "frameworks": ["GDPR", "SOC2"],
    "control_ids": ["CC6.1", "GDPR-Art-30"],
    "risk_score": 0.15
  }
}
```

---

## Policy Enforcement

### Runtime Policy Evaluation

**Real-Time Decision Engine**

Phi-Core evaluates policies in real-time:

1. **Request Received**: User attempts data access
2. **Context Gathering**: Collect user attributes, resource classification
3. **Policy Evaluation**: Run relevant policy rules
4. **Decision**: Allow, deny, or require additional approval
5. **Logging**: Record decision and rationale
6. **Enforcement**: Execute decision

**Performance**: Sub-5ms policy evaluation latency

---

### Policy Decision Points (PDP)

**Centralized Authorization**

All access decisions flow through Phi-Core's PDP:

```
Application Request
      │
      ▼
  ┌─────────────────┐
  │   Phi-Core PDP  │
  │                 │
  │ 1. Authenticate │
  │ 2. Gather Context│
  │ 3. Evaluate Policy│
  │ 4. Make Decision │
  │ 5. Log Audit    │
  └─────────────────┘
      │
      ├─> ALLOW → Grant Access
      ├─> DENY → Return 403
      └─> REQUIRE_APPROVAL → Workflow
```

**Integration Points**:
- API Gateway (pre-request authorization)
- Database proxy (row-level security)
- Object storage (pre-signed URL generation)
- File system (access control lists)

---

## Data Governance

### Data Classification

**Automatic Classification**

Phi-Core scans and classifies data:

| Classification | Examples | Access Controls | Encryption |
|---------------|----------|-----------------|------------|
| **Public** | Marketing materials | Open | Optional |
| **Internal** | Business reports | Employee-only | Standard |
| **Confidential** | Financial data | Role-based | AES-256 |
| **Restricted** | PII, PHI, PCI | Whitelist + MFA | AES-256 + HSM |

**Classification Rules**:
```yaml
classification_rules:
  - pattern: "credit_card|ccn|card_number"
    classification: restricted
    compliance: pci_dss

  - pattern: "ssn|social_security"
    classification: restricted
    compliance: hipaa

  - pattern: "email.*password"
    classification: confidential
    compliance: soc2
```

---

### Data Lineage

**Track Data Flow**

Understand data origin, transformations, and destinations:

```
Source Data (Customer DB)
  │
  ├─> ETL Process (Anonymization)
  │     └─> Analytics Warehouse
  │           └─> BI Dashboard
  │
  └─> ML Pipeline (Feature Engineering)
        └─> Model Training
              └─> Prediction API
```

**Lineage Benefits**:
- Impact analysis for schema changes
- Compliance verification (data residency)
- Debugging data quality issues
- Audit trail for sensitive data

---

## Privacy Controls

### GDPR Compliance Features

**Right to Access**
- Automated data export for user requests
- All data associated with user ID
- Machine-readable format (JSON)
- 30-day fulfillment SLA

**Right to Erasure ("Right to be Forgotten")**
- Complete data deletion across all systems
- Verification of deletion
- Audit log of erasure
- Exception handling (legal hold)

**Right to Portability**
- Export user data in structured format
- Include all consents and preferences
- Transfer to other platforms

**Consent Management**
```yaml
consent:
  user_id: user-12345
  consents:
    - purpose: marketing_emails
      granted: true
      timestamp: "2024-01-15T10:00:00Z"
      expiry: "2026-01-15T10:00:00Z"

    - purpose: analytics_tracking
      granted: false
      timestamp: "2024-01-15T10:00:00Z"
```

---

### Data Retention

**Automated Retention Policies**

```yaml
retention_policies:
  - data_type: customer_transactions
    retention_period: 7y  # Legal requirement
    archive_after: 2y
    deletion_method: secure_erase

  - data_type: audit_logs
    retention_period: 10y
    archive_after: 1y
    deletion_method: cryptographic_erasure

  - data_type: session_data
    retention_period: 30d
    archive_after: 7d
    deletion_method: soft_delete
```

**Automated Enforcement**:
- Daily scan for expired data
- Automatic archival to cold storage
- Secure deletion with verification
- Audit log of retention actions

---

## Compliance Reporting

### Automated Reports

**Available Reports**:

| Report | Frequency | Audience | Format |
|--------|-----------|----------|--------|
| **SOC 2 Evidence** | Continuous | Auditors | PDF, CSV |
| **GDPR Activity** | Monthly | DPO | PDF |
| **Access Log Summary** | Weekly | Security Team | Excel, JSON |
| **Policy Violations** | Daily | Compliance Officer | Email, Dashboard |
| **Data Classification** | Monthly | Data Governance | PDF, CSV |
| **Consent Status** | On-demand | Legal | Excel |

**Report Example**:

```yaml
report:
  type: soc2_evidence
  period: 2024-Q4
  controls:
    - control_id: CC6.1
      status: compliant
      evidence_count: 1247
      exceptions: 0
      last_test: "2024-12-15"

    - control_id: CC7.2
      status: compliant
      evidence_count: 892
      exceptions: 2
      remediation: "In progress"
```

---

### Compliance Dashboards

**Real-Time Compliance Posture**

Monitor compliance in real-time:
- **Compliance Score**: 0-100 based on controls
- **Open Issues**: Policy violations requiring attention
- **Trend Analysis**: Compliance over time
- **Framework Status**: Per-framework breakdown
- **Risk Heatmap**: High-risk areas highlighted

**Dashboard Metrics**:
```
Compliance Score: 98/100
├─ SOC 2: 100% (159/159 controls passing)
├─ GDPR: 97% (2 open consent issues)
├─ HIPAA: 100% (All controls passing)
└─ PCI DSS: 95% (1 encryption config pending)

Recent Activity:
├─ 1,234 policy evaluations (last hour)
├─ 2 policy violations (auto-remediated)
├─ 0 manual approvals pending
└─ 15 audit reports generated (today)
```

---

## Access Management

### Role-Based Access Control (RBAC)

**Pre-Defined Roles**:

| Role | Permissions | Use Case |
|------|-------------|----------|
| **Admin** | Full system access | System administrators |
| **Compliance Officer** | View all, edit policies | Compliance team |
| **Data Steward** | Classify data, review access | Data governance |
| **Auditor** | Read-only, export reports | Internal/external auditors |
| **Data Analyst** | Read classified data | Business analysts |
| **Developer** | Deploy apps, limited data access | Engineering |

**Custom Role Definition**:
```yaml
role:
  id: financial_analyst
  name: Financial Analyst
  permissions:
    - data:read:financial_data
    - reports:generate:financial_reports
    - exports:create:quarterly_summaries
  restrictions:
    data_classification: ["public", "internal", "confidential"]
    max_export_rows: 10000
    require_mfa: true
```

---

### Attribute-Based Access Control (ABAC)

**Context-Aware Authorization**

Make decisions based on attributes:

```yaml
policy:
  id: dynamic-data-access

  allow_if:
    - user.role == "analyst"
    - user.department == resource.owning_department
    - time.hour >= 9 AND time.hour <= 17  # Business hours
    - request.location == "office_network"
    - user.mfa_verified == true
```

**Supported Attributes**:
- **User**: role, department, tenure, clearance level
- **Resource**: classification, owner, sensitivity
- **Environment**: time, location, device type, network
- **Action**: read, write, delete, export

---

## Policy Testing

### Policy Validation

**Pre-Deployment Testing**

Test policies before enforcement:

```yaml
policy_test:
  policy_id: gdpr-data-access

  test_cases:
    - name: allow_with_valid_consent
      user:
        id: user-123
        consents: ["data_processing"]
      resource: customer_pii
      expected: allow

    - name: deny_without_consent
      user:
        id: user-456
        consents: []
      resource: customer_pii
      expected: deny
```

**Test Results**:
```
Running 47 policy tests...
✓ 45 passed
✗ 2 failed
  - test_expired_consent: Expected deny, got allow
  - test_multi_purpose: Expected allow, got deny

Policy validation: FAILED
Deploy blocked until issues resolved.
```

---

## Integration & Extensibility

### Webhook Integration

**Event-Driven Workflows**

Trigger external systems on policy events:

```yaml
webhooks:
  - event: policy_violation
    url: https://slack.com/api/webhook/xxx
    payload:
      text: "Policy violation detected: {{policy_id}}"
      severity: "{{violation.severity}}"

  - event: data_access_request
    url: https://approval-system.company.com/api
    payload:
      user: "{{user.email}}"
      resource: "{{resource.id}}"
      justification: "{{request.justification}}"
```

**Supported Events**:
- Policy violation
- Data access request
- Consent granted/revoked
- Retention period expiration
- Classification change
- Compliance score change

---

### API Reference

**Evaluate Policy**

**Endpoint**: `POST /api/v1/policies/evaluate`

```bash
curl -X POST https://api.veritasstack.io/v1/policies/evaluate \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "policy_id": "gdpr-data-access",
    "user_id": "user-12345",
    "resource": "customer_database.pii",
    "action": "read",
    "context": {
      "justification": "Customer support inquiry",
      "ticket_id": "SUPPORT-789"
    }
  }'
```

**Response**:
```json
{
  "decision": "allow",
  "policy_id": "gdpr-data-access",
  "evaluated_rules": 5,
  "matched_rules": ["require_consent", "audit_access"],
  "audit_id": "aud-2025-11-23-999",
  "ttl": 300
}
```

---

## Best Practices

### For Compliance Teams

1. **Start with Frameworks**: Enable relevant compliance frameworks first
2. **Review Regularly**: Monthly policy and access reviews
3. **Test Changes**: Always test policy changes in staging
4. **Document Exceptions**: Maintain clear records of policy exceptions
5. **Monitor Dashboards**: Daily compliance posture checks

### For Developers

1. **Centralize Authorization**: All access decisions through Phi-Core
2. **Handle Denials**: Gracefully handle policy denials
3. **Log Context**: Provide rich context for audit logs
4. **Test Policies**: Include policy tests in CI/CD
5. **Cache Decisions**: Cache policy decisions with appropriate TTL

### For Data Stewards

1. **Classify Data**: Ensure all data is properly classified
2. **Review Lineage**: Regular data lineage audits
3. **Update Retention**: Keep retention policies current
4. **Monitor Access**: Review access patterns for anomalies
5. **Consent Management**: Keep consent records up to date

---

## Configuration Examples

### Complete Phi-Core Configuration

```yaml
phi_core:
  # Policy engine settings
  policy_engine:
    evaluation_timeout: 5s
    cache_ttl: 300s
    strict_mode: true

  # Compliance frameworks
  compliance:
    enabled_frameworks:
      - soc2
      - gdpr
      - hipaa

    soc2:
      auditor_access: enabled
      evidence_retention: 7y

  # Data governance
  data_governance:
    auto_classification: true
    lineage_tracking: enabled
    retention_enforcement: strict

  # Audit logging
  audit:
    retention: 10y
    encryption: aes256
    export_format: json
    siem_integration: enabled

  # Privacy controls
  privacy:
    gdpr:
      right_to_access: enabled
      right_to_erasure: enabled
      right_to_portability: enabled
      consent_management: enabled
```

---

## Next Steps

- **[Security with Cerberus](cerberus.md)** - Integrate security policies
- **[Orchestration with Orion](orion.md)** - Policy-driven workload management
- **[Getting Started](../getting-started.md)** - Deploy Phi-Core
- **[Enterprise Support](../enterprise/support.md)** - Compliance consulting

---

**Questions about Phi-Core?** [Contact our compliance team](../enterprise/support.md)
