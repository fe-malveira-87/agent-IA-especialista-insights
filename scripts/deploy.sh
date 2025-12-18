#!/bin/bash
gcloud builds submit --tag gcr.io/prj-juma-farol360-poc/agente-juma-api
gcloud run deploy agente-juma-api --image gcr.io/prj-juma-farol360-poc/agente-juma-api --region us-central1 --platform managed --allow-unauthenticated