# PYTHON-RAM-FLOW 🌊

**A high-precision, real-time memory flow tracker and stress-tester for Python.**
> Stop guessing why your workers are crashing. Start auditing your memory lifecycle.

---

## Why RAM-FLOW?

### The "Monolith" Challenge
In modern Python development, projects tend to grow rapidly. What starts as a simple script often evolves into a massive Django or FastAPI monolith with dozens of applications, heavy ORM signals, and complex middleware.

In these environments, it is incredibly easy to accidentally explode host resources. A forgotten global cache, an unfiltered database cursor, or a heavy model loaded into memory creates what we call "Silent Bloat". While your script might seem to run fine once, it leaves behind a residual footprint.

In long-running worker environments (Celery, RQ), these small leaks accumulate until they trigger a catastrophic Out-Of-Memory (OOM) crash, potentially taking down your entire host. RAM-FLOW was built to detect these breakers before they reach production, giving you a surgical view of the memory lifecycle.


## 🚀 Quick Start

### Installation
```bash
pip install python-ram-flow
```

### Integrated Usage
```python
from ramflow import tracker

# 1. Capture infrastructure load (Django models, apps, etc.)
tracker.log_django_bootstrap()

@tracker.track("Oracle Data Extraction")
def process_data():
    # Your heavy logic here
    # RAM-FLOW monitors the 'Net Self' impact of this specific call
    pass

# 2. Run and Generate the Platinum Dashboard
process_data()
tracker.generate_report(suffix="nightly_sync")
```

## 📊 Visual Insights

<p align="center">
  <img src="https://github.com/addonol/python-ram-flow/blob/main/assets/02-timeline-v1.png?raw=true" width="600" alt="RAM-FLOW Dashboard">
</p>
