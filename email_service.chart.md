::: mermaid
graph TD;
    A[Start] --> B[is_valid_email]
    B --> C{Valid Email?}
    C -- No --> D[Return Invalid Email Error]
    C -- Yes --> E[get_access_token]
    E --> F{Access Token?}
    F -- No --> G[Return Access Token Error]
    F -- Yes --> H[send_email_with_attachments]
    H --> I[Prepare Email Message]
    I --> J{Attachments?}
    J -- No --> K[Send Email]
    J -- Yes --> L[Attach Files]
    L --> K[Send Email]
    K --> M{Email Sent?}
    M -- Yes --> N[Return Success]
    M -- No --> O[Return Email Sending Error]
:::