# Reference: Users API Error Resolution

## Core Behavioral Directives
* **Analyze** response headers (`Retry-After`, `X-Request-ID`) immediately when an error occurs.
* **Inspect** the `details` array in 400 responses to identify exact field failures.
* **Route** pre-migration IDs starting with `legacy_` exclusively to the `/v2/legacy-users/<id>` endpoint.
* **Format** sub-account IDs to preserve the `<parent_id>:<sub_id>` colon structure.

---

## 4xx Client Errors

### 400 Validation Failed
* **Error Code**: `validation_failed`
* **Trigger**: Missing required fields or invalid data types.
* **Resolution**: Parse the `details` array. Correct the specific fields listed.
* **Payload Example**:
```json
{
  "error": "validation_failed",
  "details": [
    {
      "field": "email",
      "reason": "invalid format"
    }
  ]
}
```

### 401 Unauthorized
* **Error Code**: `unauthorized`
* **Trigger**: Missing, malformed, or expired bearer token.
* **Resolution**: Request a new token via `/oauth/token`. Update headers. Retry request.

### 404 Not Found
* **Error Code**: `user_not_found`
* **Trigger**: Non-existent User ID or tenant mismatch.
* **Resolution**: Verify target user exists. Cross-reference request header tenant ID with user tenant ID.

### 418 Migration In Progress
* **Error Code**: `migration_in_progress`
* **Trigger**: Active schema migration. 
* **Resolution**: Pause execution for 30–60 seconds. Retry. If failure persists >5 minutes, post alert to `#data-platform`.

### 429 Rate Limited
* **Error Code**: `rate_limited`
* **Trigger**: Volume exceeded 100 requests/minute per API key.
* **Resolution**: Read the `Retry-After` header. Pause requests for the specified duration. Implement exponential backoff with jitter.

---

## 5xx Server Errors

### 502 Upstream Timeout
* **Error Code**: `upstream_timeout`
* **Trigger**: Backend service failed to respond within 30 seconds (typically during deployment restarts).
* **Resolution**: Wait 30 seconds. Retry exactly once. If second attempt fails, escalate to the on-call engineer.

### 503 Service Unavailable
* **Error Code**: `service_unavailable`
* **Trigger**: Active maintenance window or autoscaler capacity limits.
* **Resolution**: Extract `Retry-After` header value. Back off until specified time. Do not execute rapid retry loops.

### 504 Gateway Timeout
* **Error Code**: `gateway_timeout`
* **Trigger**: Internal call chain timeout.
* **Resolution**: Follow 502 retry protocol. Extract `X-Request-ID` header. Include this ID in the support ticket.

---

## Data Formatting & Routing Edge Cases

### Legacy User Routing
* **Identifier Pattern**: Begins with `legacy_` prefix (e.g., `legacy_12345`).
* **Behavior**: Standard endpoints will return a `404` error.
* **Correction**: Reroute request to `/v2/legacy-users/<id>`.

### Sub-Account ID Integrity
* **Identifier Pattern**: Compound string formatted as `<parent_id>:<sub_id>`.
* **Behavior**: Client libraries frequently strip the separating colon.
* **Correction**: Validate string structure. Re-insert the colon before initiating the retry.
