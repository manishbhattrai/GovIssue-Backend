# 🏛️ GovIssue — Infrastructure Reporting & Analytics

**GovIssue** is a high-transparency digital governance platform designed to bridge the communication gap between citizens and local authorities. It enables real-time infrastructure reporting with high-precision geolocation and provides administrators with actionable insights through specialized KPI algorithms and data-driven dashboards.

---

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-red?style=flat-square&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Stateless-blue?style=flat-square&logo=jsonwebtokens&logoColor=white)

---

## 🚀 Core Backend Logic

### 📊 Performance KPI Algorithm
Engineered a **Resolution Efficiency** metric using Django ORM aggregations to identify departmental bottlenecks.
* **Logic:** Calculates the average time delta between `created_at` and `updated_at` for issues marked as 'Resolved'.
* **Impact:** Allows officials to benchmark department speeds against the global system average.

### 💬 Recursive Discussion Engine
Developed a **self-referential database model** to support infinite nested community comments for public bulletins.
* **Optimization:** Leverages recursive `SerializerMethodField` logic to deliver deep-nested JSON structures in a single optimized request.

### ⚡ Query Optimization
Eliminated the **N+1 Query Problem** across relational endpoints by implementing `select_related` and `prefetch_related`. This reduced database hits by over 60% during high-volume feed retrieval.

---

## 🗄️ Relational Schema (MySQL)

*   **Users:** Custom model with `is_admin` boolean flags and `trust_points` gamification.
*   **Issues:** Relational mapping using UUIDs for security and ForeignKeys for Category assignment.
*   **Locations:** **One-to-One** mapping with Issues to maintain strict GPS coordinate precision.
*   **Broadcasts:** Central announcement table for administrative comment control.

---

## 🔌 API Endpoints

### Identity & Access
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/accounts/register/` | Citizen registration and profile creation |
| `POST` | `/api/accounts/login/` | JWT stateless authentication |

### Infrastructure Reports
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/issues/issue/` | Paginated feed (Supports Cursor Pagination) |
| `POST` | `/api/issues/issue/` | Multipart/Form-Data report submission |
| `PATCH` | `/api/issues/details/{id}/` | Admin status orchestration / Owner updates |
| `GET` | `/api/issues/dashboard/` | KPI analytics and system statistics |

---

## 🛠️ Setup and Installation

1. **Clone & Environment**
   ```bash
   git clone https://github.com/yourusername/govissue.git
   cd govissue

2. **Setup Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt

4. **Database Setup:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

5. **Create Superuser:**
   ```bash
   python manage.py createsuperuser

6. **Run Server:**
   ```bash
   python manage.py runserver