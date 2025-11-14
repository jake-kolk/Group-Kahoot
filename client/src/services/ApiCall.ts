import axios from 'axios';
import { defineStore } from 'pinia';
import { ref, watch } from 'vue';
import type { LoginResponse } from '../types/types';

const API_URL = 'http://localhost:8000';


export const authProvider = defineStore('authProvider', () => {
    const refresh_token = ref("");
    const access_token = ref("");
    const username = ref("");
    const userid = ref<number | null>(null);


    watch(access_token, (newToken) => {
        if (newToken){
            const getUser = async () => {
                const response = await fetchUserProfile(newToken);
                username.value = response.username;
                userid.value = response.id;
            }
            getUser();
        }
    })


    async function login(credentials: {username: string, password: string}){
        const response = await loginUser(credentials);
        if (response != undefined){
            access_token.value = response.access_token;
            refresh_token.value = response.refresh_token;
        }
        return response; 
    }

    async function register(info: {username: string, password: string, email: string}){
        await registerUser(info);
    }

    function logout() {
        refresh_token.value = "";
        access_token.value = "";
        username.value = "";
    }

    return {refresh_token, access_token, username, userid, login, register, logout}
})

const loginUser = async (credentials: { username: string; password: string }): Promise<LoginResponse | undefined> => {
    try {
        const response = await axios.post(`${API_URL}/auth/token`, credentials, {
            headers: {
                "Content-Type": "application/json",
            },
            withCredentials: true,
        });

        console.log("response data: ", response.data);
        return response.data;

    } catch (error) {
        console.log("Login error:", error);
    }
};

const registerUser = async (userInfo: {username: string, password: string, email: string}) => {
    try {
        const response = await axios.post(`${API_URL}/auth/register`, 
            userInfo,
            {
                withCredentials: true,
                headers: { "Content-Type": "application/json" }
            }
        );
        console.log("Register response data: ", response.data);
        return response.data;

    } catch (error) {
        console.log("Registration error:", error);
    }
}

const fetchUserProfile = async (token: string) => {
  try {
    console.log("FetchUserProfile token: ", token);
    const response = await axios.get(`${API_URL}/users/me`, {
    withCredentials: true,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    console.log("Fetch user profile response data: ", response.data);
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
            withCredentials: true,
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
        const response = await axios.get(`${API_URL}/question_sets/`, {
            withCredentials: true,
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
        const response = await axios.get(`${API_URL}/question_sets/${questionSetId}`, {
            withCredentials: true,
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
        const response = await axios.patch(`${API_URL}/question_sets/${questionSetId}`, updateData, {
            withCredentials: true,
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
        const response = await axios.delete(`${API_URL}/question_sets/${questionSetId}`, {
            withCredentials: true,
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
            withCredentials: true,
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
            withCredentials: true,
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
            withCredentials: true,
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
            withCredentials: true,
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
            withCredentials: true,
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

export const checkAuth = async () => {
    try {
        const response = await axios.get(`${API_URL}/auth/me`, {
            withCredentials: true // ensures cookies are sent
        });
        console.log("Logged in user:", response.data);
        return true;
    } catch (error) {
        console.log("Not authenticated:", error);
        return false;
    }
}

export const getGameServerToken = async () =>{
    try{
        const response = await axios.get(`${API_URL}/auth/game_server`, {           
            withCredentials: true // ensures cookies are sent
        });
        const token = response.data.auth_token;
        return token;
    }
    catch (error){
        console.log("Got error from getGameServerToken", error);
    }
}


