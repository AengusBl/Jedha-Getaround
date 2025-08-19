# Jedha-Getaround

This is one of several projects to hand in order to get my data science diploma. The Getaround project validates the deployment module.

[Link to the deliverable](https://aengusbl-getaround-project.hf.space)

## Contents

- Hugging_Face: The app files for the three deployments I put together
- model_training.ipynb: A Jupyter notebook containing the code I used to train the model for the prediction API.
- EDA.ipynb: Some highlights from the exploratory data analysis I went through ahead of each of the two parts of the project.
- .gitignore: Ignore this file.

## Set It Up Locally

1. In Hugging Face Spaces, create three spaces. After creating each of them, you are presented with a `git clone` command. A Hugging Face Space runs off of a Git repository and refreshes automatically when a push is performed on said repository. Run the `git clone` commands.
2. In the folders that are then created, add the contents of each of the three folders that you can find in the Hugging_Face folder of this here GitHub repository.
3. For the whole project to function properly, you need to add some secret values to the spaces. To add secrets, go to your Hugging Face space, click "Settings", and scroll down to "Variables and secrets".
4. Some of the secret values you will need come from AWS. Create an account if you don't have any.
5. In AWS, create an Amazon S3 bucket.
6. In AWS create an IAM user that has access to this S3 bucket. Make sure to keep this user's credentials.
7. Go to neon.com, create an account and create a new project.
8. Go back to Hugging Face, and add the secret values as given here. The parts in bold are the names of the secrets, and the parts after the arrows are the values of the secrets. Do not include the arrows.
    * MLFlow_tracking_server:
        * AWS_ACCESS_KEY_ID -> This is the access key ID for the IAM user you created.
        * AWS_SECRET_ACCESS_KEY -> This is the secret access key for the IAM user you created.
        * ARTIFACT_STORE_URI -> This is the resource ID of the S3 bucket you created. It should look like "s3://the-name-of-your-bucket".
        * BACKEND_STORE_URI -> This is the link you find after "psql" when pressing "Connect" in the project you created at neon.com. Make sure you got the version of the link that isn't partially hidden with asterisks.
    * pricing_API:
        * AWS_ACCESS_KEY_ID -> Same as above.
        * AWS_SECRET_ACCESS_KEY -> Same as above.
    * Main_dashboard:
        * PRICE_API_URL -> Paste here the public link to the pricing API space you created. To get a link to a space, go to your space, click the three dots next to "Settings", click on "Embed this Space", and copy the link.
        * MLFLOW_TRACKING_SERVER_URL -> Paste here the public link to the MLFlow space you created.
9. The spaces should be working.
10. You can now set up your access to the MLFlow tracking server: Create a file called ".env" outside of the folders created with the `git clone` command, and add to it the four secrets we set above. Each line should look like `SECRET_VALUE=paste_the_value_here`. Also add to it `TRACKING_SERVER_URL=link to your MLFlow space`.
11. Train a model while implementing logging through MLFlow, as seen in model_training.ipynb.
