/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-gs2yrs7r', // the auth0 domain prefix
    audience: 'hollaylovelyapi', // the audience set for the auth0 app
    clientId: 'Rbve8lS1u90LobyQ3odTNxmxaLXpKV3R', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
