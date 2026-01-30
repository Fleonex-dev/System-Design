# 💸 System Design: Payment System (Stripe)

## 🧠 The Concept
Moving money reliably. Zero tolerance for errors (double charging).

## 🛑 The Challenge (Naive Approach)
*   **Method**: Retrying on Timeout.
    *   Client sends "Charge $10".
    *   Server processes it, but Response is lost.
    *   Client sees Timeout, Retries "Charge $10".
    *   **Result**: User charged $20.

## ✅ The Solution (Optimal)
*   **Strategy**: **Idempotency Keys**.
    *   Client generates a UUID (`req_123`) *before* sending.
    *   Server checks: "Have I seen `req_123`?"
        *   If Yes: Return saved response.
        *   If No: Process charge and save ID.
*   **Reliability**: **Saga Pattern** or **Two-Phase Commit** for cross-service consistency.
