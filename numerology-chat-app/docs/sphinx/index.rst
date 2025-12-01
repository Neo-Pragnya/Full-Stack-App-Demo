Numerology Chat Application Documentation
==========================================

Welcome to the comprehensive documentation for the Numerology Chat Application - a modern, full-stack web application that combines numerology calculations with an intelligent chat interface.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   quickstart
   api/index
   guides/sphinx-guide

Overview
========

The Numerology Chat Application is a sophisticated platform that provides:

- **Comprehensive Numerology Analysis**: 15+ different numerology calculations
- **Intelligent Chat Interface**: AI-powered conversations about numerology insights
- **Modern Web Architecture**: FastAPI backend with Angular frontend
- **Production Ready**: Docker deployment with comprehensive testing

Quick Links
============

For Users
---------
- :doc:`quickstart` - Get started in 5 minutes
- :doc:`api/examples` - Usage examples  
- :doc:`api/endpoints` - API reference

For Developers  
--------------
- :doc:`guides/sphinx-guide` - Documentation guide
- :doc:`api/models` - Data models
- :doc:`overview` - Project architecture

Features
========

Numerology Calculations
-----------------------
- **Life Path Number**: Core personality traits
- **Destiny Number**: Life purpose and goals
- **Soul Urge Number**: Inner desires and motivations  
- **Personality Number**: How others perceive you
- **Master Numbers**: Special spiritual significance (11, 22, 33)
- **Karmic Lessons**: Areas for spiritual growth
- **Personal Year**: Current life cycle influences

Chat Interface
--------------
- **Context-Aware Responses**: Personalized numerology guidance
- **Interactive Feedback**: Thumbs up/down rating system
- **Session Management**: Persistent conversations
- **Natural Language**: Easy-to-understand explanations

Technical Features
------------------
- **RESTful API**: Clean, well-documented endpoints
- **Real-time Updates**: Live chat and calculations
- **Responsive Design**: Mobile-first UI/UX
- **Docker Deployment**: Containerized for easy scaling
- **Comprehensive Testing**: Unit, integration, and E2E tests

Architecture
============

::

   ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
   │   Angular       │    │   FastAPI        │    │   Numerology    │
   │   Frontend      │────│   Backend        │────│   Engine        │
   │                 │    │                  │    │                 │
   │ • Material UI   │    │ • REST API       │    │ • Calculations  │
   │ • Chat Interface│    │ • Event Tracking │    │ • Interpretations│
   │ • Responsive    │    │ • Health Checks  │    │ • Validations   │
   └─────────────────┘    └──────────────────┘    └─────────────────┘

Technology Stack
================

Backend
-------
- **FastAPI** 0.104.1 - Modern, fast web framework
- **Python** 3.11+ - Programming language  
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server implementation

Frontend
--------
- **Angular** 17 - Modern web framework
- **TypeScript** - Type-safe JavaScript
- **Angular Material** - UI component library
- **RxJS** - Reactive programming
- **SCSS** - Enhanced CSS

Infrastructure
--------------
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Production web server
- **Git** - Version control

Performance
===========

============================ ===============
Metric                       Value
============================ ===============
API Response Time            < 200ms
Chat Response Time           < 500ms  
Frontend Load Time           < 3 seconds
Bundle Size                  474KB (gzipped)
Test Coverage                > 85%
============================ ===============

Contributing
============

We welcome contributions! Please see our development guide for:

- Setting up the development environment
- Code style guidelines
- Testing requirements
- Pull request process

License
=======

This project is licensed under the MIT License - see the LICENSE file for details.

Links
=====

- `GitHub Repository <https://github.com/your-repo/numerology-chat-app>`_
- `Live Demo <https://demo.numerology-chat.com>`_
- `API Documentation <http://localhost:8000/docs>`_
- `Issue Tracker <https://github.com/your-repo/numerology-chat-app/issues>`_

---

*Last updated: November 30, 2025*