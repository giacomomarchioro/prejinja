# Multilinguism a short introduction

When we are developing a website we might have to take into account that the
visitors might come from different regions and use different languages.

[Google Developers guide](https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites)
gives some suggestions to increase the usability of the website:
 - Use different URL for each page:
   -  example.com/de/ ✅
   -  de.example.com ✅
   -  example.de ✅
 - Don't use cookies or query parameters:
   -  site.com?loc=de 🚫
 - Use `herflang` annotations for different versions of the same page.


```html
<link rel="alternate" hreflang="x" href="https://esempio.com/pagina-alternativa" />
```


```html
<html lang="fr" xml:lang="fr" xmlns="http://www.w3.org/1999/xhtml">
```




# Javascript
Many of the localization procedure can be performed client-side using javascript.

## Numbers

```javascript
123.4.toLocaleString('ar-EG')
```


### Currency

```javascript
data.toLocaleString('it-IT', {style: 'currency', currency: 'EUR'})
```

## Dates

```javascript
const event = new Date(Date.UTC(2012, 11, 20, 3, 0, 0));
const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
console.log(event.toLocaleDateString('de-DE', options));
```

## Quotes
Quotes vary depending on the region a particular case are the German quotes.

Make sure quotes are set to auto in your CSS file:
```css
quotes: auto;
```
## Part in different languages

```
<p lang="fr">Ceci est un paragraphe.</p>
```

@@part in a different lang@@[it]

## Region vs language
Some users might use a different language that is not spoken in the region.

In this case we can use the time zone:

```javascript
Intl.DateTimeFormat().resolvedOptions().timeZone
```

## Checks
You can check for problems using:
https://validator.w3.org/i18n-checker/