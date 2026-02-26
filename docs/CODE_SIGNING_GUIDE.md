# Windows SmartScreen & Code Signing Guide

**Issue:** Windows shows "Windows protected your PC" warning when running Calcora.exe  
**Impact:** Destroys user trust, blocks adoption  
**Priority:** CRITICAL for v0.3.0 success  

---

## 🔍 Why This Happens

Windows SmartScreen blocks unsigned executables from unknown publishers. This affects:
- All PyInstaller apps (Calcora included)
- Any unsigned .exe downloaded from the internet
- New publishers without "reputation"

**This is NOT a malware detection** — it's lack of digital signature + low download count.

---

## 🚀 Solutions (Priority Order)

### ⚡ **Immediate Actions (Today - Free)**

#### 1. Generate File Checksums
Provide SHA256 hash for users to verify integrity:

```powershell
# Generate checksums
Get-FileHash .\dist\Calcora.exe -Algorithm SHA256 | Format-List

# Add to release notes:
# SHA256: [hash will be here]
```

#### 2. Submit to Microsoft SmartScreen
Tell Microsoft the file is safe (builds reputation over time):

**Steps:**
1. Go to: https://www.microsoft.com/en-us/wdsi/filesubmission
2. Upload: `Calcora.exe`
3. Category: "Software Developer"
4. Description: "Open-source mathematical computation desktop app"
5. Submit for review

**Timeline:** 1-7 days for review, reputation builds over weeks

#### 3. Update Release Notes
Add "Security & Trust" section explaining the warning:

```markdown
### ⚠️ Windows SmartScreen Warning (Expected)

**You may see:** "Windows protected your PC" when first running Calcora.exe

**Why?** Calcora is not yet code-signed (requires paid certificate). This is a 
standard warning for new open-source applications.

**Is it safe?**
✅ Source code is publicly auditable on GitHub  
✅ Built with PyInstaller (industry-standard Python packager)  
✅ No telemetry, no network calls (100% offline)  
✅ SHA256 checksum provided for verification  

**To run anyway:**
1. Click "More info"
2. Click "Run anyway"

**Coming in v0.3.1:** Code-signed executable (no warning)
```

---

### 🛡️ **Short-Term Solution (1-2 Weeks - $100-500/year)**

#### Get Code Signing Certificate

**What it does:**
- Digitally signs the .exe with your identity
- Tells Windows "This file is from a verified publisher"
- Eliminates SmartScreen warning IMMEDIATELY after signing

**Certificate Providers (Trusted by Windows):**

1. **SSL.com** (Recommended for open source)
   - Cost: $199/year (individual), $299/year (organization)
   - Fast approval (1-3 days)
   - eSigner cloud signing (USB not required)
   - Link: https://www.ssl.com/certificates/code-signing/

2. **Sectigo (Comodo)**
   - Cost: $179/year (individual)
   - Good reputation
   - Physical USB token required

3. **DigiCert**
   - Cost: $469/year (organization only)
   - Premium option, best for commercial

**For Open Source Projects:**
Some CAs offer discounts for verified open-source projects.

#### Verification Requirements

**Individual Code Signing:**
- Government-issued ID
- Phone number verification
- Email verification
- Takes: 1-3 business days

**Organization Code Signing:**
- Business registration documents
- D-U-N-S number (optional but helps)
- Takes: 3-7 business days

#### After Getting Certificate

**Windows Signing Process:**
```powershell
# Install certificate (provided by CA)
# Then sign the executable:

signtool sign /f "certificate.pfx" /p "password" /tr http://timestamp.sectigo.com /td sha256 /fd sha256 "dist\Calcora.exe"

# Verify signature:
signtool verify /pa "dist\Calcora.exe"
```

**Add to build script:**
```powershell
# build-desktop.ps1 (after PyInstaller)

if (Test-Path "cert\calcora-codesign.pfx") {
    Write-Info "Signing executable..."
    signtool sign /f "cert\calcora-codesign.pfx" /p $env:CERT_PASSWORD /tr http://timestamp.sectigo.com /td sha256 /fd sha256 "dist\Calcora.exe"
    Write-Success "✓ Executable signed"
} else {
    Write-Warning "⚠ Certificate not found - executable unsigned"
}
```

---

### 🏆 **Long-Term Solution (Optional - $474/year)**

#### Extended Validation (EV) Code Signing

**Benefits:**
- **INSTANT** SmartScreen trust (no reputation period needed)
- Shows organization name in UAC prompts
- Highest trust level

**Cost:** ~$474/year (DigiCert, Sectigo)

**Requirements:**
- Must be organization (not individual)
- Physical USB token shipped to business address
- More rigorous verification (7-14 days)

**Worth it?** Only if you're releasing frequently or need immediate trust.

---

## 📋 **Action Plan for v0.3.0**

### Phase 1: Today (Free, Immediate)
```powershell
# 1. Generate checksum
Get-FileHash .\dist\Calcora.exe -Algorithm SHA256 | Tee-Object -Variable hash
Write-Output "SHA256: $($hash.Hash)" | Out-File checksums.txt

# 2. Update release notes with checksum + warning explanation

# 3. Submit to Microsoft SmartScreen
#    https://www.microsoft.com/en-us/wdsi/filesubmission

# 4. Publish v0.3.0 with disclaimer
```

### Phase 2: This Week (Paid)
```
1. Choose certificate provider (SSL.com recommended)
2. Apply for individual code signing cert ($199/year)
3. Complete verification (1-3 days)
4. Sign Calcora.exe
5. Release v0.3.1 (signed)
```

### Phase 3: Ongoing (Reputation Building)
```
- Each download/run builds SmartScreen reputation
- After ~50-100 successful runs, warning may disappear even for unsigned
- Signed version builds reputation faster
```

---

## 💰 **Budget Considerations**

| Solution | Cost | Timeline | Effectiveness |
|----------|------|----------|---------------|
| Checksums + Docs | $0 | Today | Low (explains, doesn't fix) |
| SmartScreen Submit | $0 | 1-7 days review, weeks for reputation | Medium (slow) |
| Code Signing (Individual) | $199/year | 1-3 days | **High (immediate)** |
| Code Signing (Org) | $299/year | 3-7 days | High |
| EV Code Signing | $474/year | 7-14 days | Highest (instant trust) |

**Recommended:** Get individual code signing cert ($199/year) — best ROI for trust.

---

## 🔒 **Security Best Practices**

**For Users (Add to README):**
```markdown
### Verifying Download Integrity

Before running Calcora.exe, verify the checksum:

```powershell
# Windows PowerShell
Get-FileHash Calcora.exe -Algorithm SHA256

# Expected hash:
# SHA256: [hash from release notes]
```

If hashes match → safe to run!
```

**For Developers (Build Transparency):**
- Publish checksums with every release
- Document build process in DESKTOP_GUIDE.md
- Keep source code visible on GitHub
- Use GitHub Actions for reproducible builds

---

## 📚 **Additional Resources**

- **Microsoft SmartScreen Submission:** https://www.microsoft.com/en-us/wdsi/filesubmission
- **Code Signing Guide:** https://learn.microsoft.com/en-us/windows/win32/seccrypto/cryptography-tools
- **SSL.com Code Signing:** https://www.ssl.com/certificates/code-signing/
- **PyInstaller Security:** https://pyinstaller.org/en/stable/usage.html#using-upx

---

## 🎯 **v0.3.1 Goals**

**Must Have:**
- ✅ Code-signed executable (no SmartScreen warning)
- ✅ SHA256 checksums in release notes
- ✅ Security verification section in README

**Nice to Have:**
- ⏳ Automated signing in build script
- ⏳ GitHub Actions builds with signing
- ⏳ Multi-platform signing (macOS notarization)

---

## ⚠️ **Important Notes**

1. **Don't self-sign** — Windows doesn't trust self-signed certificates
2. **Use timestamp server** — Certificate expiry won't invalidate old signatures
3. **Protect certificate** — Never commit `.pfx` files to Git
4. **Annual renewal** — Budget for yearly certificate renewal
5. **Reputation takes time** — Even signed apps need initial downloads to build trust

---

**Next Step:** Generate checksums and update release notes today, then order code signing certificate this week.
