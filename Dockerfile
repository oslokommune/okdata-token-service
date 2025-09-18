FROM public.ecr.aws/lambda/python:3.11

COPY token_service/main ${LAMBDA_TASK_ROOT}/token_service/main
COPY serverless/documentation/schemas ${LAMBDA_TASK_ROOT}/serverless/documentation/schemas
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

RUN yum install shadow-utils -y
RUN /sbin/groupadd -r app
RUN /sbin/useradd -r -g app app
RUN chown -R app:app ${LAMBDA_TASK_ROOT}
USER app

CMD ["set-me-in-serverless.yaml"]
