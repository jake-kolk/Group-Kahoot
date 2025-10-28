import axios from 'axios';
import { defineStore } from 'pinia';

const API_URL = 'https://localhost:8000';

export const authKey = defineStore('authKey', {
    state: () => ({
        token: ''
    }),
    actions: {
        setToken(newToken: string) {
            this.token = newToken;
        }
    }
})

export const loginUser = async (credentials: {username: string, password: string}) => {
    try {
        const params = new URLSearchParams();
        for (const key in credentials) {
        params.append(key, credentials[key as keyof typeof credentials]);
    }

        const response = await axios.post(`${API_URL}/auth/token`, credentials, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });
    console.log("response data: ", response.data);
    authKey().setToken(response.data.access_token);
    return response.data;
    }catch (error) {
        console.log("Login error:", error);
    }
};

export const registerUser = async (userInfo: {username: string, password: string, email: string}) => {
    try {
        const response = await axios.post(`${API_URL}/auth/register`, userInfo);
        return response.data;
    } catch (error) {
        console.log("Registration error:", error);
    }
}

export const fetchUserProfile = async (token: string) => {
  try {
    console.log("FetchUserProfile token: ", token);
    const response = await axios.get(`${API_URL}/users/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    return response.data;
  } catch (error) {
    console.log("Fetch user profile error: ", error);
    throw error;
  }
};

//
// 
//

export const createQuestionSet = async (token: string, questionSetData: {title: string, description?: string}) => {
    try {
        const response = await axios.post(`${API_URL}/questionsets/`, questionSetData, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Create question set error:", error);
        throw error;
    }
};

export const fetchAllQuestionSets = async (token: string) => {
    try {
        const response = await axios.get(`${API_URL}/questionsets/`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Fetch question sets error:", error);
        throw error;
    }
};

export const fetchQuestionSet = async (token: string, questionSetId: number) => {
    try {
        const response = await axios.get(`${API_URL}/questionsets/${questionSetId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Fetch question set error:", error);
        throw error;
    }
};

export const updateQuestionSet = async (token: string, questionSetId: number, updateData: {title?: string, description?: string}) => {
    try {
        const response = await axios.patch(`${API_URL}/questionsets/${questionSetId}`, updateData, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Update question set error:", error);
        throw error;
    }
};

export const deleteQuestionSet = async (token: string, questionSetId: number) => {
    try {
        const response = await axios.delete(`${API_URL}/questionsets/${questionSetId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Delete question set error:", error);
        throw error;
    }
};

export const createQuestion = async (token: string, questionData: {question_set: number, question_text: string, choices: string[], correct_answer: string, time_limit: number}) => {
    try {
        const response = await axios.post(`${API_URL}/questions/`, questionData, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Create question error:", error);
        throw error;
    }
};

export const fetchAllQuestions = async (token: string, questionSetId: number) => {
    try {
        const response = await axios.get(`${API_URL}/questions/?question_set=${questionSetId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Fetch questions error:", error);
        throw error;
    }
};

export const fetchQuestion = async (token: string, questionId: number) => {
    try {
        const response = await axios.get(`${API_URL}/questions/${questionId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Fetch question error:", error);
        throw error;
    }
};

export const updateQuestion = async (token: string, questionId: number, updateData: {question_text?: string, choices?: string[], correct_answer?: string, time_limit?: number}) => {
    try {
        const response = await axios.patch(`${API_URL}/questions/${questionId}`, updateData, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Update question error:", error);
        throw error;
    }
};

export const deleteQuestion = async (token: string, questionId: number) => {
    try {
        const response = await axios.delete(`${API_URL}/questions/${questionId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        return response.data;
    } catch (error) {
        console.log("Delete question error:", error);
        throw error;
    }
};
