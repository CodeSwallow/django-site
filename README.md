# CodeSwallow site for writing articles and blogs created using Django Framework

Simple article/blog site created using Django and deployed using AWS Elastic Beanstalk. For template styling, Bootstrap v5.3 was used.

## Website URL
https://codeswallow.com/ (Changing to another AWS account, currently down)

## Tech Stack
- Python 3.8
- Django
- Bootstrap v5.3
- AWS Elastic Beanstalk for deployment
- AWS RDS for database
- AWS S3 for serving static files
- AWS SES for password reset through email
- CodeCommit (original repository)

## Features:
### Main page with list of articles and featured posts:
![codeswallow site image](https://irs-github-images.s3.amazonaws.com/codeswallo_site/codeswallow-site.png)

### Post body and table of content using python-markdown:
![post detail image](https://irs-github-images.s3.amazonaws.com/codeswallo_site/post-detail.png)

### Search for name or category of post:
![post search image](https://irs-github-images.s3.amazonaws.com/codeswallo_site/post-search.png)

### Login or create an account:
![login image](https://irs-github-images.s3.amazonaws.com/codeswallo_site/login.png)

### Post comments:
![comments image](https://irs-github-images.s3.amazonaws.com/codeswallo_site/comments.png)

## Upcoming features:
1. AWS Cognito for user signing, currently is using Django's authentication system.
2. New comment system (Disqus?)
3. Dark/light mode
