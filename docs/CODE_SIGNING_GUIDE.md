# Code Signing Notes

So Windows is throwing that annoying "Windows protected your PC" message when people try to run Calcora. It's expected (we're not signed yet), but it looks sketchy to users who don't know better.

## Why This Happens

Windows SmartScreen flags unsigned executables from unknown publishers. Since we're using PyInstaller and don't have a code signing cert yet, Windows doesn't trust us. It's not malware detection - just lack of digital signature + low reputation score.

## Quick Fixes

### Right Now (Free)

**Generate checksums for integrity verification:**

```powershell
Get-FileHash .\dist\Calcora.exe -Algorithm SHA256
```

Add the resulting hash to release notes so users can verify they got the real deal.

**Submit to Microsoft SmartScreen:**
https://www.microsoft.com/en-us/wdsi/filesubmission

Upload Calcora.exe, mark it as safe software. Takes 1-7 days for review, then reputation builds gradually over time.

**Update docs to explain the warning:**

Tell users in the README and release notes that the warning is expected, how to bypass it ("More info" → "Run anyway"), and that v0.3.1 will have a signed exe. Also mention the checksum verification.

### Near Term ($199/year)

**Get a code signing certificate:**

This is the real solution. Sign the exe with a trusted cert and the warning disappears immediately.

**Recommended providers:**
- **SSL.com** - $199/year for individuals, fast approval (1-3 days), cloud signing (no USB token needed)
- **Sectigo** - $179/year, good reputation, requires physical USB token
- **DigiCert** - $469/year, premium option

For open source projects, might be able to get a discount if we reach out.

**Verification requirements:**
- Government ID
- Phone + email verification
- Takes 1-3 business days for individual certs

**Once we have the cert:**

```powershell
# Sign the exe (add this to build script)
signtool sign /f "cert.pfx" /p $env:CERT_PASSWORD /tr http://timestamp.sectigo.com /td sha256 /fd sha256 "dist\Calcora.exe"

# Verify it worked
signtool verify /pa "dist\Calcora.exe"
```

Make sure to use a timestamp server so the signature stays valid even after the cert expires.

### Long Term (Optional - $474/year)

**Extended Validation (EV) code signing:**

This gives **instant** SmartScreen trust (no reputation building period needed) and shows our org name in UAC prompts. But it requires:
- Business entity (not individual)
- Physical USB token
- More rigorous verification (7-14 days)
- Higher cost

Probably not worth it unless we're releasing frequently or need immediate trust. Standard code signing works fine once reputation builds.

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

## Action Plan

### Phase 1: Today
1. Generate SHA256 checksum of Calcora.exe
2. Add checksum + warning explanation to release notes
3. Submit exe to Microsoft SmartScreen
4. Update README with security verification section

### Phase 2: This Week
1. Apply for SSL.com individual code signing cert ($199/year)
2. Complete verification (1-3 days)
3. Sign Calcora.exe
4. Release v0.3.1 with signed executable

### Phase 3: Ongoing
Each download builds SmartScreen reputation. After ~50-100 successful runs, the warning might disappear even for unsigned builds (but better to just stay signed).

## Budget

| Solution | Cost | Timeline | Impact |
|----------|------|----------|--------|
| Checksums + docs | $0 | Today | Low (just explains the warning) |
| SmartScreen submit | $0 | 1-7 days review + weeks for reputation | Medium (slow build) |
| Code signing cert | $199/year | 1-3 days | **High (immediate fix)** |
| EV code signing | $474/year | 7-14 days | Highest (instant trust) |

Recommendation: Get the $199/year cert. Best value for eliminating the warning.

## Security Notes

**For users (add to README):**
```markdown
### Verifying Download

Before running Calcora.exe, verify the checksum:

```powershell
Get-FileHash Calcora.exe -Algorithm SHA256
# Expected: [hash from release notes]
```

If it matches, you're good to go.
```

**For the build:**
- Never commit .pfx cert files to git
- Store cert password in environment variable
- Use timestamp server so signatures remain valid after cert expires
- Keep build process documented and transparent

## Resources

- Microsoft SmartScreen submission: https://www.microsoft.com/en-us/wdsi/filesubmission
- SSL.com code signing: https://www.ssl.com/certificates/code-signing/
- Microsoft code signing docs: https://learn.microsoft.com/en-us/windows/win32/seccrypto/crystography-tools

## Important

- Don't use self-signed certs (Windows won't trust them)
- Use timestamp servers (signatures stay valid after cert expiry)
- Protect the certificate file (never commit to version control)
- Budget for annual renewal

## Next Steps

Generate checksums and update docs today, then order the cert this week. Should have signed builds for v0.3.1.
