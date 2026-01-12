# Quick Deploy to Netlify

## One-Click Deploy

[![Deploy to Netlify](https://www.netlify.com/img/deploy/button.svg)](https://app.netlify.com/start/deploy?repository=https://github.com/YOUR-USERNAME/calcora)

## Manual Deploy (5 minutes)

### 1. Prerequisites
- GitHub account with your Calcora repository
- Netlify account (free)

### 2. Connect Repository
1. Go to [netlify.com](https://netlify.com)
2. Click "Add new site" → "Import an existing project"
3. Connect GitHub → Select `calcora` repository
4. Netlify auto-detects settings from `netlify.toml`

### 3. Deploy
Click "Deploy site" and wait 3-5 minutes for the first build.

### 4. Get Your URL
You'll receive: `https://random-name.netlify.app`

Optional: Customize to `calcoralive.netlify.app` in Site settings → Domain management

### 5. Test
- Landing page: `https://YOUR-SITE.netlify.app/`
- **Interactive demo**: `https://YOUR-SITE.netlify.app/demo.html` ← Share this!

## What Gets Deployed

✅ Static documentation site  
✅ Interactive browser demo (differentiation + matrix operations)  
✅ Python serverless function (Calcora engine backend)  
✅ HTTPS enabled automatically  
✅ CDN for fast global access  

## Sharing with Universities

Share this link format:
```
https://YOUR-SITE-NAME.netlify.app/demo.html
```

Example message:
```
I've built Calcora, an open-source math computation engine with 
step-by-step explanations. Try the live demo:

https://calcoralive.netlify.app/demo.html

Test examples:
- Differentiate: sin(x^2)
- Matrix determinant: [[1,2],[3,4]]
- Symbolic: [["a","b"],["c","d"]]

Source: github.com/YOUR-USERNAME/calcora
```

## Updating Your Demo

Every time you push to GitHub `main` branch:
```bash
git add .
git commit -m "Update demo"
git push origin main
```
Netlify automatically redeploys in 1-2 minutes.

## Troubleshooting

**Build fails?**  
Check Netlify dashboard → Deploys → Build logs

**Function errors?**  
Check Netlify dashboard → Functions → calcora_engine → Logs

**Need help?**  
See full guide: [DEPLOYMENT.md](DEPLOYMENT.md)

## Free Tier Limits

✅ 125,000 function calls/month  
✅ 100GB bandwidth  
✅ Unlimited sites  
✅ Free HTTPS  

Perfect for university demo and portfolio showcase!
