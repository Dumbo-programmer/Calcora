# Calcora v0.2-alpha Release Notes

**Release Date**: January 13, 2026  
**Major Focus**: Integration Engine & Academic Adoption Strategy

## 🎯 Vision Update

Calcora is evolving from a computational tool to an **academic platform** designed for universities, STEM students, and researchers. Our goal is to become the preferred alternative to WolframAlpha by emphasizing:

- **Educational transparency**: Step-by-step explanations that teach, not just compute
- **Research reproducibility**: Open-source, auditable computations
- **Accessibility**: Zero cost, offline-first, privacy-respecting
- **Modern UX**: Beautiful, intuitive interface with interactive visualizations

## 🆕 Major Features

### 1. Integration Engine

The integration engine is the cornerstone of Calcora v0.2, essential for any calculus course.

**Capabilities:**
- ✅ **Indefinite integrals** with automatic technique selection
- ✅ **Definite integrals** using Fundamental Theorem of Calculus
- ✅ **Multiple techniques**: Power rule, substitution, integration by parts, trigonometric
- ✅ **Step-by-step explanations** with rule names and detailed reasoning
- ✅ **Verbosity levels**: Concise, detailed, or teacher mode
- ✅ **Interactive graphs**: Area under curve visualization

**Supported Integration Techniques:**
1. **Power Rule**: ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C
2. **Substitution**: For expressions like ∫ f(g(x))·g'(x) dx
3. **Integration by Parts**: For products like ∫ x·eˣ dx
4. **Trigonometric**: For sin, cos, tan and their powers
5. **General**: Fallback to SymPy's integrate() for complex cases

**API Usage:**
```python
from calcora.integration_engine import IntegrationEngine

engine = IntegrationEngine()

# Indefinite integral
result = engine.integrate("x**2", variable="x", verbosity="detailed")
# Output: x**3/3 + C
# Steps: ["Using power rule: ∫ xⁿ dx = xⁿ⁺¹/(n+1) + C"]

# Definite integral
result = engine.integrate(
    "x**2", 
    variable="x", 
    lower_limit=0, 
    upper_limit=1,
    verbosity="teacher"
)
# Output: 0.333333333333333 (or 1/3)
# Steps: ["Power rule", "Fundamental theorem: F(b) - F(a)"]
```

**HTTP API:**
```bash
POST http://localhost:8000/api/compute
Content-Type: application/json

{
  "operation": "integrate",
  "expression": "x**2",
  "variable": "x",
  "lower_limit": "0",
  "upper_limit": "1",
  "verbosity": "detailed"
}
```

### 2. Enhanced UI

**New Integration Tab:**
- Quick example chips: x², sin(x), cos²(x), eˣ, 1/x, x·eˣ, √x
- Expression input with syntax helper
- Variable selector
- Definite integral toggle with bound inputs
- Verbosity level selector
- Graph toggle for area visualization
- Modern glassmorphism design

**Improvements:**
- Tab navigation between Differentiation, Integration, and Matrix operations
- Consistent design across all operation types
- Better error messages with syntax guidance
- Real-time validation

### 3. Academic Strategy Document

Created comprehensive [ACADEMIC_STRATEGY.md](ACADEMIC_STRATEGY.md) outlining:

**Phase 1 (Weeks 1-8): Essential Calculus Features**
- ✅ Integration engine (COMPLETED!)
- Series expansion (Taylor/Maclaurin)
- Limits computation
- LaTeX export
- Equation solving

**Phase 2 (Weeks 9-16): Research Features**
- Advanced matrix operations (SVD, QR, eigenvectors)
- 3D visualization
- Batch computation API
- Citation export
- Jupyter notebook integration

**Success Metrics (6 months):**
- 1,000 GitHub stars
- 50 universities aware of Calcora
- 10,000 monthly active users
- 10 research papers citing Calcora
- 5 university partnerships

**Marketing Strategy:**
- Demo videos on YouTube
- Academic paper submission
- University outreach program
- Reddit/HackerNews launch
- Conference presentations

### 4. Documentation Updates

**README.md:**
- Updated status to v0.2-alpha
- Added "Vision: Academic Adoption" section
- Listed new integration features
- Updated feature list and examples
- Added "What's New in v0.2" section

**New Test Suite:**
- `test_integration_api.py`: Comprehensive API testing
- Tests for power rule, trig, exponential, definite integrals
- Integration by parts candidates
- Error handling verification

## 📊 Technical Details

**New Files:**
- `src/calcora/integration_engine.py` (300+ lines)
- `ACADEMIC_STRATEGY.md` (comprehensive roadmap)
- `test_integration_api.py` (API test suite)

**Modified Files:**
- `src/calcora/api/main.py` (added integration endpoint)
- `site/demo.html` (added integration tab, ~90 lines)
- `README.md` (updated with v0.2 info)

**Code Quality:**
- Type hints throughout IntegrationEngine
- Comprehensive docstrings
- Error handling for edge cases
- Extensible architecture for new techniques

**Architecture:**
```
IntegrationEngine
├── integrate() - Main entry point
├── _determine_technique() - Automatic technique selection
├── _integrate_power_rule() - For polynomials
├── _integrate_substitution() - For composite functions
├── _integrate_by_parts() - For products
├── _integrate_trig() - For trigonometric functions
└── _evaluate_definite() - Apply bounds using FTC
```

## 🧪 Testing

All integration tests pass successfully:

```
✅ ∫ x² dx = x³/3 + C
✅ ∫ sin(x) dx = -cos(x) + C
✅ ∫ eˣ dx = eˣ + C
✅ ∫₀¹ x² dx = 1/3 ≈ 0.333
✅ ∫ x·eˣ dx = (x-1)·eˣ + C
✅ ∫ cos²(x) dx = x/2 + sin(x)cos(x)/2 + C
```

Run tests: `python test_integration_api.py`

## 🚀 Deployment

**Backend (Render):**
- Build: `pip install sympy fastapi "uvicorn[standard]" && pip install -e .`
- Start: `uvicorn calcora.api.main:app --host 0.0.0.0 --port $PORT`
- URL: https://calcora.onrender.com

**Frontend (Netlify):**
- Build: Copy `site/` directory
- URL: https://calcoralive.netlify.app

**Local Development:**
```bash
# Terminal 1: Backend
cd b:\Development\Calcora
python -m uvicorn calcora.api.main:app --reload

# Terminal 2: Frontend
cd b:\Development\Calcora\site
python -m http.server 5000

# Open: http://localhost:5000/demo.html
```

## 📝 What's Next

### Immediate (This Week)
- Add more integration examples to UI
- Improve error messages for unsupported integrals
- Add technique hints before computation
- Create demo video showcasing integration

### Phase 1 Priority (Next 2 Months)
1. **Series Expansion** (2 weeks)
   - Taylor series around x=a
   - Maclaurin series (Taylor around x=0)
   - Order selection
   - Convergence information

2. **Limits** (2 weeks)
   - One-sided limits
   - Limits at infinity
   - L'Hôpital's rule application
   - Indeterminate forms

3. **LaTeX Export** (1 week)
   - Export full computation as LaTeX document
   - Include steps and graphs
   - Citation-ready format

4. **Equation Solving** (2 weeks)
   - Algebraic equations
   - Transcendental equations
   - Systems of equations
   - Symbolic solutions

### Long-term (6 months)
- Jupyter notebook kernel
- VS Code extension
- Mobile-responsive design
- Collaborative features
- University partnerships

## 🎓 For Educators

Calcora v0.2 is designed with educators in mind:

**Classroom Benefits:**
- **No internet required**: Run entirely offline in computer labs
- **Transparent**: Students see every step, understanding the "why"
- **Free forever**: Zero licensing costs for schools
- **Privacy-first**: No student data collection
- **Customizable**: Verbosity levels for different learning stages

**Homework Integration:**
- Students can verify their work
- Teachers can check solution methods
- Step-by-step output helps identify misconceptions
- Graph visualizations aid understanding

**Research Applications:**
- Reproducible computations
- Export to LaTeX for papers
- Batch processing for data analysis
- Open-source for audit and extension

## 🤝 Contributing

We're actively seeking contributors, especially:

- **Mathematicians**: Help improve technique detection and explanations
- **Educators**: Provide feedback on pedagogical value
- **Students**: Test features and report usability issues
- **Developers**: Add new operations and improve architecture

**Priority Areas:**
1. Series expansion implementation
2. Limit computation engine
3. LaTeX export formatting
4. UI/UX improvements
5. Documentation and tutorials

See [ACADEMIC_STRATEGY.md](ACADEMIC_STRATEGY.md) for detailed roadmap.

## 📜 License

MIT License - Free for academic and commercial use

## 🙏 Acknowledgments

This release represents a major step toward making Calcora a serious academic tool. Special thanks to:
- SymPy project for symbolic mathematics foundation
- FastAPI for excellent API framework
- Chart.js for beautiful visualizations
- KaTeX for math rendering

---

**GitHub**: https://github.com/Dumbo-programmer/Calcora  
**Demo**: https://calcoralive.netlify.app  
**Issues**: https://github.com/Dumbo-programmer/Calcora/issues

Let's build the future of mathematical computation together! 🚀📐
