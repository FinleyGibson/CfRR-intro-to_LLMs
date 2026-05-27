# New Course Checklist and Timeline

## **In August**

- [x] Before the academic year in which the course will run, you should confirm the topic and high-level overview with CfRR Programme Management

## **12 weeks before delivery**

- [x] Confirm the details of the delivery team from CfRR Admin (CodingForReproducibleResearch@exeter.ac.uk)
- [x] Identify materials reviewer for **materials appropriateness** review (a subject matter expert who will assess whether the content is accurate, complete, and suitable for the intended audience; this review is separate from the functionality and accessibility review conducted later). You may wish to draw upon the CfRR Content Advisory Group described on the roles page [here](roles.ipynb). For new courses, also determine which Content Advisory Group area the course sits within, or identify a suitable advisor if a new area is needed.
- [x] Schedule recurring team check-ins
- [x] Open GitHub Issue for the new course; create feature branch in [CfRR_Courses repo](https://github.com/coding-for-reproducible-research/CfRR_Courses)
- [x] Draft **course objectives** and detailed **learning objectives** for each section of the course
- [x] Identify a high-level timeline for content creation

## **8 weeks before delivery**

### Course Confirmation and Scheduling

- [x] Confirm course outcomes and pre-requisites with CfRR Admin (CodingForReproducibleResearch@exeter.ac.uk) to facilitate timely scheduling and promotion.

## **6 weeks before delivery**

### Content Completion

- [ ] Submit first complete draft of materials to the branch
- [x] Populate `programme_information`
- [x] Populate `section_landing_page`
- [x] Populate `where_is_my_understanding` quiz
    - `JSON` files confirmed to render via `JupyterQuiz`
- [x] Add an entry to `data/course_style.csv` to specify the course style (e.g. Live Coding, Seminar, Hybrid)
- [x] Add course pages to `_toc.yml`
- [ ] Check for overlapping or missing sections

### Technical Validation

- [ ] Test interactive plots, embedded HTML, and widgets
- [ ] Validate quiz rendering (`display_quiz("path/to/quiz.json")`)
- [ ] Verify all file paths use **relative paths** for Jupyter Book
- [ ] Confirm all assets (images, data files, HTML) load correctly
- [ ] Include slides/PDFs as required and confirm static content links
- [ ] Execute all notebooks end-to-end

### Review and Quality Assurance

- [ ] Website functionality review (navigation, rendering, interactivity)
    - [ ] Assigned to Liam Berrisford (GitHub: @liamjberrisford)
    - [ ] Covers: `_toc.yml`, interactive elements, embedded content
- [ ] Materials appropriateness review (clarity, level, pedagogical fit)
    - [ ] Assigned to designated reviewer
    - [ ] Covers: markdown content, exercises, quizzes, learning flow
- [ ] Code and documentation peer review
    - [ ] Covers: code comments, markdown explanations, notebook structure
- [ ] Ensure all licences and terms relevant to the course are explicitly documented in the materials (software/packages, services/platforms, datasets/content), including any attribution, redistribution, or usage restrictions.

## **4 weeks before delivery**

- [ ] Address all outstanding feedback from reviews
- [ ] Confirm all assets are correctly linked and functional
- [ ] Ensure Continuous Integration (CI) build for Jupyter Book passes, including accessibility checks

## **2 weeks before delivery**

- [ ] Freeze content
- [ ] Perform final proofreading and “top-to-bottom” notebook execution
- [ ] Notify Liam Berrisford (GitHub: @liamjberrisford) that materials are ready for integration into the website
- [ ] Obtain final sign-off from Liam Berrisford (GitHub: @liamjberrisford)
- [ ] Merge feature branch into main
- [ ] Notify [Jenny McGarvey](https://libguides.exeter.ac.uk/prf.php?id=b1cb0409-e2fc-11ef-b755-0647746d9baf) of the upcoming course
