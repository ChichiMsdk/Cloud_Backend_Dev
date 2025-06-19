# Assignment Cloud Backend Developer 

> Only Part 1 is required, Part 2 is just to score some extra points.
> The goal is to deliver a minimum viable product. 
> Write the _simplest_ view providing “useful rated feedback” about a web application.

## Must do
  - Feedback: a rated statement about the application, very general or very specific. 

  - Examples:
    * Bad: This application is crap 
    * Good (but): I would like to have a reduced loading time 
    * Bad: The application freezes all the time. 
    * Very Good (but): I miss feature XYZ 
    * Good (but): The new version XYZ introduces bug ABC 

  - Useful feedback is one discussed by the whole user community and mitigated by comments / notation (+1, 0, 1). 
  - The comments are used in order to discuss and ideally scope the statement.
  - A user can give several comments or feedback.
  - The notation enables to mitigate the importance of the feedback. A user can only give 1 notation to feedback. 

## Objectives
Develop an API that can be provided to the front-end team in Python and following RESTful principles.

### Part 1: User Feedback list (*required*) 
A user of a web-based application has a view to post feedback with at least: 
1) a note (optional description of the issue) 
2) a rating 1=bad, 5=very good). 

For each entry, another view which to browse the feedback comments and performing:
1) Add a comment to the feedback 
2) Give a (+1, 0, 1) notation to other user’s comments 

### Part 2: Product Manager view (*optional*) 

1) Manager's abilities:
  - Put the user feedback into categories
  - Give feedback's status:
    * Open 
    * Closed (backlog) 
    * Closed (solved) 
    * Closed (rejected) 
 - Merge similar feedback.

2) Implementing some unit tests is a plus. 

## Delivery 
You will need to send me an email that includes links to the following: 
  - The source code itself hosted on Github. 
  - A hosted version of the application for us to test. I recommend using Github Pages.
When reviewing the application, we will be focusing on: 
  - Your understanding of the programming paradigms (asynchronicity, prototyping, etc.)
  - Robustness and error handling 
  - Code quality and best practices (testing strategy) 
  - Code style and attention to detail 
  - Documentation
