# coculatex
A command-line utility that creates the new LaTeX project from the LaTex project parameterised template.

__NOTE__. Please notes. This project is active development. At now, there is no stable version of it.

We will demonstrate the basic idea of our project by example.

Let there is the `LaTeX` theme 'myarticle'. It has the following files:
myarticle_template.tex - jinja2 template
```latex
\documentclass[twoside]{article}
\usepackage[english]{babel}
\usepackage{mytitle.sty}

\begin{document}
    \mytitle{\VAR{title}}
    \maketitle
    \VAR{tex_main}
\end{document}
 ```
mytitle.sty - additional styling file 
example.tex - the example for the theme:
```text
 Hello, World!
```

Further, You have the configuration file mypaper.yaml:

```yaml
theme: myarticle
title: Hello document
```

Because the mypaper.source.tex does not exist, in the result of the running script would be created files:
mypaper.source.tex:
```latex
%!TEX root=mypaper.tex
Hello, World!
```

mypaper.tex:
```latex
\documentclass[twoside]{article}
\usepackage[english]{babel}
\usepackage{mytitle.sty}

\begin{document}
    \mytitle{Hello document}
    \maketitle
    \VAR{mypaper.source.tex}
\end{document}
```
mystyle.sty

And now you can compile the LaTeX source.
