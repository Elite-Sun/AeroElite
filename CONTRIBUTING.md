# Contributing to Aero Elite

Thank you for your interest in contributing to Aero Elite! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/AeroElite.git`
3. Create a branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Test your changes
6. Commit: `git commit -m "Add feature: description"`
7. Push: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

See [SETUP.md](SETUP.md) for detailed setup instructions.

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions and classes
- Maximum line length: 100 characters

```python
def generate_wing(
    wingspan_m: float,
    chord_m: float,
    airfoil: str = "NACA2412"
) -> cq.Workplane:
    """
    Generate parametric wing model.

    Args:
        wingspan_m: Wingspan in meters
        chord_m: Chord length in meters
        airfoil: Airfoil designation

    Returns:
        CadQuery workplane with wing geometry
    """
    pass
```

### TypeScript/React (Frontend)

- Use functional components with hooks
- Follow React best practices
- Use TypeScript strict mode
- Use Material-UI components

```typescript
interface WingProps {
  wingspan: number;
  chord: number;
  airfoil: string;
}

const Wing: React.FC<WingProps> = ({ wingspan, chord, airfoil }) => {
  // Component implementation
};
```

## Testing

### Backend

```bash
cd backend
pytest tests/ -v --cov=app
```

### Frontend

```bash
cd frontend
npm test
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Areas for Contribution

### High Priority

- [ ] Improve CAD generation accuracy
- [ ] Add more airfoil profiles
- [ ] Enhance physics validation
- [ ] Implement full CFD integration
- [ ] Add manufacturing export (CNC, 3D printing)

### Medium Priority

- [ ] Mobile app development
- [ ] Collaborative design features
- [ ] Real-time collaboration
- [ ] Advanced materials database
- [ ] Cost estimation module

### Documentation

- [ ] Video tutorials
- [ ] API examples
- [ ] Best practices guide
- [ ] Architecture diagrams

## Reporting Issues

Use GitHub Issues with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Environment details (OS, Python/Node version)

## Questions?

Open a GitHub Discussion or contact: dev@aeroelite.com
