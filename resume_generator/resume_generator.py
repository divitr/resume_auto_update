import json
import os
import subprocess
from datetime import datetime

general_info = r"""
%-------------------------
% Resume in Latex
% Author : Jake Gutierrez
% Based off of: https://github.com/sb2nov/resume
% License : MIT
%------------------------

\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}


%----------FONT OPTIONS----------
% sans-serif
% \usepackage[sfdefault]{FiraSans}
% \usepackage[sfdefault]{roboto}
% \usepackage[sfdefault]{noto-sans}
% \usepackage[default]{sourcesanspro}

% serif
% \usepackage{CormorantGaramond}
% \usepackage{charter}


\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubSubheading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \textit{\small#1} & \textit{\small #2} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%


\begin{document}

"""
header = r"""
%----------HEADING----------
% \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
%   \textbf{\href{http://sourabhbajaj.com/}{\Large Sourabh Bajaj}} & Email : \href{mailto:sourabh@sourabhbajaj.com}{sourabh@sourabhbajaj.com}\\
%   \href{http://sourabhbajaj.com/}{http://www.sourabhbajaj.com} & Mobile : +1-123-456-7890 \\
% \end{tabular*}

\begin{center}
    \textbf{\Huge \scshape Divit Rawal} \\ \vspace{1pt}
    \small (425)-309-0699 $|$ \href{mailto:divit.rawal@gmail.com}{\underline{divit.rawal@gmail.com}} $|$ 
    \href{https://www.divitrawal.com}{\underline{divitrawal.com}} $|$
    \href{https://www.github.com/divitr/}{\underline{github.com/divitr}}
\end{center}

"""
    
def convert_to_latex(resume_data, resume_type):
    latex_output = general_info + header

    for section_name, section_data in resume_data.items():
        latex_output += f"\\section{{{section_name.title()}}}\n"
        if section_name == "education":
            for entry in section_data:
                    if resume_type in entry['category']:
                        latex_output += "  \\resumeSubHeadingListStart\n"
                        latex_output += f"    \\resumeSubheading\n      {{{entry['info']['name']}}}{{{entry['info']['dates']}}}\n      {{{entry['info']['major']}}}{{{entry['info']['location']}}}\n"

                        if 'bullets' in entry['info']:
                            latex_output += "      \\resumeItemListStart\n"
                            for bullet in entry['info']['bullets']:
                                latex_output += f"        \\resumeItem{{{bullet}}}\n"
                            latex_output += "      \\resumeItemListEnd\n"

                        latex_output += "  \\resumeSubHeadingListEnd\n\n"
        elif section_name == "experience":
            for entry in section_data:
                if resume_type in entry['category']:
                    latex_output += "  \\resumeSubHeadingListStart\n"
                    latex_output += f"    \\resumeSubheading\n      {{{entry['info']['company']}}}{{{entry['info']['dates']}}}\n      {{{entry['info']['title']}}}{{{entry['info']['location']}}}\n"

                    if 'bullets' in entry['info']:
                        latex_output += "      \\resumeItemListStart\n"
                        for bullet in entry['info']['bullets']:
                            latex_output += f"        \\resumeItem{{{bullet}}}\n"
                        latex_output += "      \\resumeItemListEnd\n"

                    latex_output += "  \\resumeSubHeadingListEnd\n\n"
        elif section_name == "projects":
            for entry in section_data:
                if resume_type in entry['category']:
                    latex_output += "  \\resumeSubHeadingListStart\n"
                    latex_output += f"    \\resumeProjectHeading\n      {{\\textbf{{{entry['info']['name']}}} $|$ \\emph{{{entry['info']['skills']}}}}}{{{entry['info']['dates']}}}\n"

                    if 'bullets' in entry['info']:
                        latex_output += "      \\resumeItemListStart\n"
                        for bullet in entry['info']['bullets']:
                            latex_output += f"        \\resumeItem{{{bullet}}}\n"
                        latex_output += "      \\resumeItemListEnd\n"

                    latex_output += "  \\resumeSubHeadingListEnd\n\n"
        elif section_name == "technical skills":
            latex_output += "   \\begin{itemize}[leftmargin=0.15in, label={}] \n    \\small{\\item{\n"
            for key, value in section_data.items():
                latex_output += f"      \\textbf{{{key.title()}}}: {value}"
                if key != list(section_data.keys())[-1]:
                    latex_output += "\\\\\n"
                else:
                    latex_output += "\n"
            latex_output += "       }}\n\end{itemize}"
    latex_output += "\n\n\\end{document}"

    return latex_output

resume_types = ["master", "physics", "cs", "tutoring", "test"]

with open("/Users/divitrawal/Desktop/resume/resume_data.json", "r") as file:
        resume_data = json.load(file)

for resume_type in resume_types:
    latex = convert_to_latex(resume_data, resume_type)
    os.makedirs(f"/Users/divitrawal/Desktop/resume/{resume_type}", exist_ok=True)
    with open(f"/Users/divitrawal/Desktop/resume/{resume_type}/resume_{resume_type}.tex", "w+") as resume:
        resume.write(latex)
    subprocess.call(["pdflatex", f"-output-directory=/Users/divitrawal/Desktop/resume/{resume_type}/", f"/Users/divitrawal/Desktop/resume/{resume_type}/resume_{resume_type}.tex"])
    with open(f"/Users/divitrawal/Desktop/resume/{resume_type}/timestamp.txt", "w+") as timestamp_file:
        timestamp_file.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    with open("/Users/divitrawal/Desktop/resume/resume_generator/resume_types.txt", "r") as typetxt:
        existing_resume_types = typetxt.read().splitlines()
    if resume_type not in existing_resume_types:
        with open("/Users/divitrawal/Desktop/resume/resume_generator/resume_types.txt", "a") as typetxt:
            typetxt.write(f"\n{resume_type}")