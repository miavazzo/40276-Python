::: mermaid
graph TD
    A[Start] --> B[send_email Route]
    B --> C[Log Received request to /send_email]
    C --> D[Log Request Headers]
    D --> E[Check API Key]
    E --> F{API Key Valid?}
    F -- No --> G[Log Unauthorized access attempt]
    G --> H[Return 401 Unauthorized]
    F -- Yes --> I[Log API key authentication successful]
    I --> J[Parse JSON Data]
    J --> K{JSON Valid?}
    K -- No --> L[Log Error parsing JSON]
    L --> M[Return 400 Invalid JSON]
    K -- Yes --> N[Check Required Fields]
    N --> O{All Fields Present?}
    O -- No --> P[Log Missing required field]
    P --> Q[Return 400 Missing Parameter]
    O -- Yes --> R[Log All required fields are present]
    R --> S[Save Attachments]
    S --> T[Log Calling send_email_with_attachments function]
    T --> U[Call send_email_with_attachments]
    U --> V[Remove Temporary Files]
    V --> W[Log Email sending attempt completed]
    W --> X[Return Email Sending Result]

    A --> Y[ping Route]
    Y --> Z[Log Received request to /ping]
    Z --> AA[Return API is reachable]
:::