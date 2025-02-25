  import React from "react";
  // import background from '../../assets/image/cut.png'
  import { useState } from "react";
  const background = require("../../assets/image/cut.png");

  import { Link, useNavigate } from "react-router-dom";
  import { Spinner, Alert } from "flowbite-react";
  import { signInStart, signInSuccess, signInFailure } from "../../redux/user/userSlice";
  
  import { useDispatch, useSelector } from "react-redux";


  interface RootState {
    user: {
      currentUser: null | any;
      loading: boolean;
      error: string | null;
    }
  }
  export default function Login() {
    const [formData, setFormData] = useState({
        email_username: "",
        password: "",
    
    });
    const dispatch = useDispatch();
    const { loading, error: errorMessage } = useSelector((state: RootState) => state.user);
    const navigate = useNavigate();
    
    const handleChange  = (e) => {
      setFormData({...formData, [e.target.id]: e.target.value.trim()});

    }

    const handleSubmit = async (e) => {
      e.preventDefault();
      if (!formData.email_username || !formData.password) {
         return dispatch(signInFailure("All fields are required!"));
      }
  
      try {
        dispatch(signInStart());
        const isEmail = formData.email_username.includes("@");
        const requestBody = {
          email: isEmail ? formData.email_username : undefined,
          username: !isEmail ? formData.email_username : undefined,
          password: formData.password,
        };
        const res = await fetch("http://localhost:8001/api/auth/signin", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        });
       
        const data = await res.json();
        if (res.status === 200 && data.success) {
          dispatch(signInSuccess(data));
          navigate("/home");
        } else {
          dispatch(signInFailure(data.message));
          
        }
      } catch (error){
        dispatch(signInFailure(error.message));
        
      }
      
    }
    console.log(formData);
    return (
      <div className="font-[sans-serif]">
        <div className="flex flex-col items-center justify-center w-full h-screen">
          <div className="grid md:grid-cols-2  gap-4 max-md:gap-8 max-w-full w-full h-full m-0 rounded-md flex-col items-center justify-center">
            <div className="flex flex-col items-center justify-center">
              <div className="m-3 md:max-w-md w-full flex flex-col items-center justify-center">
                  <form className="w-full max-w-sm" onSubmit={handleSubmit}>
                    <div className="mb-12 flex flex-col items-center justify-center">
                      <h3 className="text-gray-800 text-4xl font-bold">Welcome back!</h3>
                      <p className="text-sm mt-4 text-gray-800">Don't have an account 
                        <Link to="/register" className="text-blue-600 font-semibold hover:underline ml-1 whitespace-nowrap">Register here</Link>
                      </p>
                    </div>

                    <div>
                      {/* <label className="text-gray-800 text-xs block mb-2">Email</label>
                      <div className="relative flex items-center">
                        <input name="email" type="text" id="email"  required onChange={handleChange} className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" placeholder="name@gmail.com" />
                        <svg xmlns="http://www.w3.org/2000/svg" fill="#bbb" stroke="#bbb" className="w-[18px] h-[18px] absolute right-2" viewBox="0 0 682.667 682.667">
                          <defs>
                            <clipPath id="a" clipPathUnits="userSpaceOnUse">
                              <path d="M0 512h512V0H0Z" data-original="#000000"></path>
                            </clipPath>
                          </defs>
                          <g clip-path="url(#a)" transform="matrix(1.33 0 0 -1.33 0 682.667)">
                            <path fill="none" stroke-miterlimit="10" stroke-width="40" d="M452 444H60c-22.091 0-40-17.909-40-40v-39.446l212.127-157.782c14.17-10.54 33.576-10.54 47.746 0L492 364.554V404c0 22.091-17.909 40-40 40Z" data-original="#000000"></path>
                            <path d="M472 274.9V107.999c0-11.027-8.972-20-20-20H60c-11.028 0-20 8.973-20 20V274.9L0 304.652V107.999c0-33.084 26.916-60 60-60h392c33.084 0 60 26.916 60 60v196.653Z" data-original="#000000"></path>
                          </g>
                        </svg>
                      </div> */}
                      <label className="text-gray-800 text-xs block mb-2">Email hoặc Username</label>
                      <div className="relative flex items-center">
                        <input 
                            name="email_username" 
                            type="text" 
                            id="email_username"  
                            required 
                            onChange={handleChange} 
                            className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" 
                            placeholder="Nhập email hoặc username" />
                      </div>
                    </div>

                    <div className="mt-8">
                      <label className="text-gray-800 text-xs block mb-2">Password</label>
                      <div className="relative flex items-center">
                        <input name="password" type="password" id="password" required onChange={handleChange} className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" placeholder="Enter password" />
                        <svg xmlns="http://www.w3.org/2000/svg" fill="#bbb" stroke="#bbb" className="w-[18px] h-[18px] absolute right-2 cursor-pointer" viewBox="0 0 128 128">
                          <path d="M64 104C22.127 104 1.367 67.496.504 65.943a4 4 0 0 1 0-3.887C1.367 60.504 22.127 24 64 24s62.633 36.504 63.496 38.057a4 4 0 0 1 0 3.887C126.633 67.496 105.873 104 64 104zM8.707 63.994C13.465 71.205 32.146 96 64 96c31.955 0 50.553-24.775 55.293-31.994C114.535 56.795 95.854 32 64 32 32.045 32 13.447 56.775 8.707 63.994zM64 88c-13.234 0-24-10.766-24-24s10.766-24 24-24 24 10.766 24 24-10.766 24-24 24zm0-40c-8.822 0-16 7.178-16 16s7.178 16 16 16 16-7.178 16-16-7.178-16-16-16z" data-original="#000000"></path>
                        </svg>
                      </div>
                    </div>

                    {/* <div className="flex flex-wrap items-center justify-between gap-4 mt-6">
                      <div className="flex items-center">
                        <input id="remember-me" name="remember-me" type="checkbox" className="h-4 w-4 shrink-0 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                        <label htmlFor="remember-me" className="ml-3 block text-sm text-gray-800">
                          Remember me
                        </label>
                      </div>
                      <div>
                        <a href="javascript:void(0);" className="text-blue-600 font-semibold text-sm hover:underline">
                          Forgot Password?
                        </a>
                      </div>
                    </div> */}

                    <div className="mt-8">
                      {/* <Link to="/home"> */}
                        <button type="submit" 
                        disabled={loading}

                        className="w-full shadow-xl py-1 px-4 text-sm tracking-wide rounded-md text-white bg-green-700 hover:bg-green-800 focus:outline-none">
                          {loading ? (
                            <>
                              <Spinner size="sm" />
                              <span className="pl-3">Loading...</span>
                            </>
                          ) : (
                            "Login"
                          )}
                        </button>
                      {/* </Link> */}
                      {errorMessage && (<Alert className="mt5 text-red-500" >{errorMessage}</Alert>)} 
                    </div>
                           
                    <div className="flex items-center justify-center mt-9 mb-9">
                      <div className="flex-grow border-t border-gray-300"></div>
                      <span className="mx-4 text-black-500">Or</span>
                      <div className="flex-grow border-t border-gray-300"></div>
                    </div>

                    
                  </form>
                  
                  <div className="max-w-sm mx-auto mt-6 border rounded-lg shadow-lg p-0.5 bg-white cursor-pointer hover:bg-gray-100">
                      <div className="space-x-4 flex justify-center">
                        <div className="flex items-center ml-5">
                            <button type="button" className="border-none outline-none">
                              <svg xmlns="http://www.w3.org/2000/svg" width="20px" className="inline" viewBox="0 0 512 512">
                                <path fill="#fbbd00" d="M120 256c0-25.367 6.989-49.13 19.131-69.477v-86.308H52.823C18.568 144.703 0 198.922 0 256s18.568 111.297 52.823 155.785h86.308v-86.308C126.989 305.13 120 281.367 120 256z" data-original="#fbbd00" />
                                <path fill="#0f9d58" d="m256 392-60 60 60 60c57.079 0 111.297-18.568 155.785-52.823v-86.216h-86.216C305.044 385.147 281.181 392 256 392z" data-original="#0f9d58" />
                                <path fill="#31aa52" d="m139.131 325.477-86.308 86.308a260.085 260.085 0 0 0 22.158 25.235C123.333 485.371 187.62 512 256 512V392c-49.624 0-93.117-26.72-116.869-66.523z" data-original="#31aa52" />
                                <path fill="#3c79e6" d="M512 256a258.24 258.24 0 0 0-4.192-46.377l-2.251-12.299H256v120h121.452a135.385 135.385 0 0 1-51.884 55.638l86.216 86.216a260.085 260.085 0 0 0 25.235-22.158C485.371 388.667 512 324.38 512 256z" data-original="#3c79e6" />
                                <path fill="#cf2d48" d="m352.167 159.833 10.606 10.606 84.853-84.852-10.606-10.606C388.668 26.629 324.381 0 256 0l-60 60 60 60c36.326 0 70.479 14.146 96.167 39.833z" data-original="#cf2d48" />
                                <path fill="#eb4132" d="M256 120V0C187.62 0 123.333 26.629 74.98 74.98a259.849 259.849 0 0 0-22.158 25.235l86.308 86.308C162.883 146.72 206.376 120 256 120z" data-original="#eb4132" />
                              </svg>
                            </button>
                          </div>
                          <div>
                            <p className="text-base mt-1">
                            Sign in with Google
                            </p>
                          </div>
                        </div>
                      </div>     
              </div>
            </div>

            <div className="md:h-full rounded-xl relative bg-cover bg-center" style={{ backgroundImage: `url(${background})` }}>
              <div className="absolute inset-0 bg-black opacity-20 rounded-xl"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }