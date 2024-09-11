import axios, { AxiosResponse } from 'axios';

export class Albergue {
    private configuration: any;

    constructor(configuration?: any) {
        this.configuration = configuration;
    }

    public async removeUser() {
        try {
            await axios.post(`${this.configuration.basePath}/logout/`, {}, {
                withCredentials: true
            });

        } catch (error) {
            console.error("Error al intentar realizar logout:", error);
        }
    }

    // Refrescar el access token usando el refresh token
    async refreshToken(callback: () => void) {
        try {
            const response = await axios.post(`${this.configuration.basePath}/token/refresh/`, {}, {
                withCredentials: true  // Enviar automáticamente las cookies con la solicitud
            });
            callback();  // Realizar el callback si se renovó el token correctamente
        } catch (error) {
            console.error("Error al refrescar el token:", error);
            this.removeUser();
        }
    }

    async get(path: string, requestParams: any = null, callback: (response: AxiosResponse<any>) => any, errorCallback?: (error: any) => void) {
        axios.get(
            this.configuration.basePath + path,
            {
                params: requestParams ? requestParams : {},
                withCredentials: true  // Enviar automáticamente las cookies con la solicitud
            },
        ).then(callback).catch(error => {
            if (error.response && error.response.status === 401) {
                this.refreshToken(() => {
                    this.get(path, requestParams, callback, errorCallback);
                });
            } else {
                console.error("GET request error:", error);
                if (errorCallback) {
                    errorCallback(error);
                }
            }
        });
    }

    async post(path: string, requestBody: any, callback: (response: AxiosResponse<any>) => any, errorCallback?: (error: any) => void) {
        axios.post(
            this.configuration.basePath + path,
            requestBody,
            {
                withCredentials: true  // Enviar automáticamente las cookies con la solicitud
            },
        ).then(response => {
            callback(response);
        }).catch(error => {
            if (error.response && error.response.status === 401) {
                this.refreshToken(() => {
                    this.post(path, requestBody, callback, errorCallback);
                });
            } else {
                console.error("POST request error:", error);
                if (errorCallback) {
                    errorCallback(error);
                }
            }
        });
    }

    async put(path: string, requestBody: any, callback: (response: AxiosResponse<any>) => any, errorCallback?: (error: any) => void) {
        axios.put(
            this.configuration.basePath + path,
            requestBody,
            {
                withCredentials: true  // Enviar automáticamente las cookies con la solicitud
            },
        ).then(response => {
            callback(response);
        }).catch(error => {
            if (error.response && error.response.status === 401) {
                this.refreshToken(() => {
                    this.put(path, requestBody, callback, errorCallback);
                });
            } else {
                console.error("PUT request error:", error);
                if (errorCallback) {
                    errorCallback(error);
                }
            }
        });
    }

    async patch(path: string, requestBody: any, callback: (response: AxiosResponse<any>) => any, errorCallback?: (error: any) => void) {
        axios.patch(
            this.configuration.basePath + path,
            requestBody,
            {
                withCredentials: true  // Enviar automáticamente las cookies con la solicitud
            },
        ).then(response => {
            callback(response);
        }).catch(error => {
            if (error.response && error.response.status === 401) {
                this.refreshToken(() => {
                    this.patch(path, requestBody, callback, errorCallback);
                });
            } else {
                console.error("PATCH request error:", error);
                if (errorCallback) {
                    errorCallback(error);
                }
            }
        });
    }
}

const configuration = {
    basePath: 'http://127.0.0.1:8000/api',
    headers: {
        "Content-Type": "application/json",
    }
};

export const AlbergueAPIClient = new Albergue(configuration);
