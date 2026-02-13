# 🧠 Django Online Test Application

A full-stack Online Test Platform built using Django that enables users to take timed assessments, submit answers, and receive instant results.
This project simulates a real-world online examination system with secure authentication, timer-based submission, automated evaluation, and an admin-managed question system.

## ✨ Key Features

- 🔐 Secure User Authentication (Register / Login / Logout)
- 📝 Attempt MCQ-Based Online Tests
- ⏳ Timer-Based Auto Submission
- 📊 Automatic Score Calculation
- 📈 Result Dashboard
- 🛠 Admin Panel for Question Management
- 🎯 Clean & Responsive UI
- 🗄 Structured Database Design

### 👤 User Flow

1. User registers or logs in.
2. User starts the test.
3. Timer begins automatically.
4. User selects answers.
5. Test auto-submits when timer ends (or manual submit).
6. Backend evaluates responses.
7. Final score is displayed instantly.

---

## 🗄 Database Design Overview

- **User** – Authenticated test takers
- **Question** – Stores question text
- **Option / Choice** – Linked to questions
- **Correct Answer** – Stored for evaluation
- **TestAttempt** – Tracks user attempts
- **Result** – Stores score and attempt details

<img width="1898" height="972" alt="Screenshot 2026-02-13 223845" src="https://github.com/user-attachments/assets/82c54155-bc24-4900-b7fe-c19a8131b908" />

<img width="1915" height="975" alt="Screenshot 2026-02-13 223920" src="https://github.com/user-attachments/assets/5b09d97d-4c96-43e1-89e8-66cfd5f1d6e3" />

<img width="1294" height="697" alt="Screenshot 2026-02-13 223955" src="https://github.com/user-attachments/assets/e5f69309-ab26-48c6-af1d-4259cb2e0f73" />

<img width="1875" height="973" alt="Screenshot 2026-02-13 224025" src="https://github.com/user-attachments/assets/0111a54c-1af2-4fbb-906c-8c5462a7bd10" />



