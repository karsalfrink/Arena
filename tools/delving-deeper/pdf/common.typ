// Shared page setup and front matter for the Delving Deeper reference PDFs.

#let setup(title, doc) = {
  set page(
    paper: "a4",
    margin: (x: 18mm, top: 18mm, bottom: 20mm),
    footer: context [
      #set text(size: 8pt)
      #set align(center)
      #title · #counter(page).display("1 / 1", both: true)
    ],
  )
  set text(font: "Libertinus Serif", size: 9.5pt, lang: "en", region: "GB")
  set par(justify: false, leading: 0.55em)
  show heading.where(level: 1): it => block(above: 0pt, below: 4mm)[
    #set text(size: 18pt, weight: "bold")
    #it.body
  ]
  show heading.where(level: 2): it => block(above: 6mm, below: 2.5mm)[
    #set text(size: 11pt, weight: "bold")
    #it.body
  ]
  show heading.where(level: 3): it => block(above: 3mm, below: 1.5mm)[
    #set text(size: 9.5pt, weight: "bold")
    #it.body
  ]
  show link: underline
  doc
}

// The front note: what Delving Deeper is, where the numbers come from,
// where the source lives and how the work was done.
#let front-note(d, extra) = [
  #set text(size: 9pt)
  #set par(leading: 0.5em)
  *Delving Deeper* is a retroclone of the original 1974 edition of the
  fantasy role-playing game, written by Simon J. Bull and published by
  Immersive Ink (#link("https://ddo.immersiveink.com/")[ddo.immersiveink.com]).
  This document is modelled on Dan Collins's OED handouts of the same name
  (#link("https://oedgames.com/")[oedgames.com]). Every value comes from
  #raw(d.csv), an Arena monster database of the Delving Deeper reference
  rules; the Equivalent Hit Dice (EHD) were computed by running Dan's Arena
  combat simulator on the Delving Deeper statistics. The database and the
  script that produced this document live in
  #link(d.repo)[github.com/karsalfrink/Arena], directory
  `tools/delving-deeper/`; the database is proposed upstream in
  #link(d.pr)[danielrcollins1/Arena pull request 6]. The database and this
  document were produced with a large language model (Anthropic's Claude)
  under the review of Kars Alfrink; the README in that directory says how.
  #extra
  Generated from #raw(d.csv) at commit #raw(d.version.commit) (#d.version.date).
]
