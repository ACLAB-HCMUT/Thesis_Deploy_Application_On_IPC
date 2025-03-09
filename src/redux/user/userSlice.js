import {createSlice} from "@reduxjs/toolkit";

const initialState = {
    currentUser: null,
    loading: false,
    error: null,
}

const userSlice = createSlice({
    name: "user",
    initialState,
    reducers: {
        signInStart: (state) => {
            state.loading = true;
            state.error = null;
        },
        signInSuccess: (state, action) => {
            state.currentUser = action.payload;
            state.access_token = action.payload.access_token;
            state.refresh_token = action.payload.refresh_token;
            state.loading = false;
            state.error = null;
        },
        signInFailure: (state, action) => {
            
            state.loading = false;
            state.error = action.payload;
        },
        logout: (state) => {
            state.currentUser = null;
            state.access_token = null;
            state.refresh_token = null;
            state.loading = false;
            state.error = null;
        },
    },
});


export  const { signInStart, signInSuccess, signInFailure, logout } = userSlice.actions;

export default userSlice.reducer;