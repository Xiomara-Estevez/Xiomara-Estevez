const awsconfig = {
  Auth: {
    region: "us-east-2",
    userPoolId: "us-east-2_OKfpu9Y8n",
    userPoolWebClientId: "101hsgmv9a4jr6pe2qnma58faj",
  },
  API: {
    endpoints: [
      {
        name: "telehealthAPI",
        endpoint: "https://te1uy0vqw5.execute-api.us-east-2.amazonaws.com/dev",
      },
    ],
  },
  Storage: {
    AWSS3: {
      bucket: "tthealth-telehealthdocumentsbucket-jn3k6z7uroyp",
      region: "us-east-2",
    },
  },
};

export default awsconfig;
