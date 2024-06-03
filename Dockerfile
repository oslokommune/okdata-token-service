FROM public.ecr.aws/lambda/python:3.11

COPY token_service/main ${LAMBDA_TASK_ROOT}/token_service/main
COPY serverless/documentation/schemas ${LAMBDA_TASK_ROOT}/serverless/documentation/schemas
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

CMD ["set-me-in-serverless.yaml"]
