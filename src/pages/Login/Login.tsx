import React from "react";
// import background from '../../assets/image/cut.png'
import { useState, useEffect } from "react";
import CryptoJS from "crypto-js";
import { Link, useNavigate } from "react-router-dom";
import { Spinner, Alert } from "flowbite-react";
import { signInStart, signInSuccess, signInFailure } from "../../redux/user/userSlice";
import { useDispatch, useSelector } from "react-redux";
import { Phone, Eye, EyeOff } from "lucide-react";


// Load environment variables from .env file
import { SECRET_KEY } from '../../config/env.tsx';
const background = require("../../assets/image/farmer.jpg");




interface RootState {
  user: {
    currentUser: null | any;
    access_token: string | null;
    refresh_token: string | null;
    loading: boolean;
    error: string | null;
  }
}
export default function Login() {
  const [formData, setFormData] = useState({
      email_phone: "",
      password: "",
  
  });
  const [showPassword, setShowPassword] = useState(false); // State cho xem/ẩn password
  const [rememberMe, setRememberMe] = useState(false); // State cho remember me
  const dispatch = useDispatch();
  const { loading, error: errorMessage } = useSelector((state: RootState) => state.user);
  const navigate = useNavigate();
  
  // Load dữ liệu từ localStorage khi trang khởi tạo
  useEffect(() => {
    const savedEmail = localStorage.getItem("savedEmail");
    const savedPasswordEncrypted = localStorage.getItem("savedPassword");
    if (savedEmail && savedPasswordEncrypted) {
      try {
        // Kiểm tra xem savedPassword có phải là chuỗi mã hóa không
        const bytes = CryptoJS.AES.decrypt(savedPasswordEncrypted, SECRET_KEY);
        const decryptedPassword = bytes.toString(CryptoJS.enc.Utf8);
        if (decryptedPassword) {
          setFormData({
            email_phone: savedEmail,
            password: decryptedPassword,
          });
          setRememberMe(true);
        } else {
          // Nếu không giải mã được, xóa dữ liệu cũ
          console.log("Invalid encrypted password, clearing localStorage");
          localStorage.removeItem("savedEmail");
          localStorage.removeItem("savedPassword");
        }
      } catch (error) {
        console.error("Failed to decrypt password:", error);
        localStorage.removeItem("savedEmail");
        localStorage.removeItem("savedPassword");
      }
    }
  }, []);

  const handleChange  = (e) => {
    setFormData({...formData, [e.target.id]: e.target.value.trim()});

  }
  const toggleShowPassword = () => {
    setShowPassword((prev) => !prev);
  };
  // Hàm lưu tokens vào localStorage
  const storeTokens = (access_token, refresh_token, email) => {
    localStorage.setItem("access_token", access_token);
    localStorage.setItem("refresh_token", refresh_token);
    localStorage.setItem("userEmail", email);
    if (rememberMe) {
      console.log("Saving to localStorage with rememberMe:", formData);
      if (!formData.email_phone || !formData.password) {
        console.error("Email or password is empty, cannot save to localStorage");
        return;
      }
      localStorage.setItem("savedEmail", formData.email_phone);
      const encryptedPassword = CryptoJS.AES.encrypt(formData.password, SECRET_KEY).toString();
      console.log("Encrypted password:", encryptedPassword); // Debug
      localStorage.setItem("savedPassword", encryptedPassword);
    } else {
      localStorage.removeItem("savedEmail");
      localStorage.removeItem("savedPassword");
    }
  };
// Hàm refresh token
const refresh_token = async () => {
  try {
      const refresh_token = localStorage.getItem('refresh_token');
      // const res = await fetch("http://localhost:8001/api/auth/refresh-token", {
      //     method: "POST",
      //     headers: {
      //         "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify({ refreshToken }),
      // });
      // const res = await fetch("http://localhost:8000/api/users/refresh-token", {
      const res = await fetch("http://localhost:3000/api/users/refresh-token", {  
      method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ refresh_token }),

    });

      const data = await res.json();
      if (res.status === 201 && data.success) {
          storeTokens(data.access_token, data.refresh_token, data.data.email);
          dispatch(signInSuccess({
              user: data.data,
              access_token: data.access_token,
              refresh_token: data.refresh_token
          }));
          return data.access_token;
      } else {
          throw new Error("Refresh token failed");
      }
  } catch (error) {
      dispatch(signInFailure("Session expired. Please login again."));
      navigate("/login");
      throw error;
  }
};

const handleSubmit = async (e) => {
  e.preventDefault();
  console.log("1. Form submitted:", formData);

  if (!formData.email_phone || !formData.password) {
    console.log("2. Missing fields, dispatching failure");
    return dispatch(signInFailure("All fields are required!"));
  }

  try {
    console.log("3. Starting sign-in process");
    dispatch(signInStart());
    const requestBody = { email: formData.email_phone, password: formData.password };
    console.log("4. Request body:", requestBody);

    const res = await fetch("http://localhost:3000/api/users/signin", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(requestBody),
    });
    console.log("5. Fetch completed, status:", res.status);

    const data = await res.json();
    console.log("6. Response data:", data);

    if ((res.status === 200 || res.status === 201) && data.success) {
      console.log("7. Sign-in successful");
      const email = data.data.email;
      storeTokens(data.access_token, data.refresh_token, email);
      dispatch(signInSuccess({ 
        user: data.data, 
        access_token: data.access_token, 
        refresh_token: data.refresh_token 
      }));
      navigate("/home");
    } else {
      console.log("8. Sign-in failed with message:", data.message);
      dispatch(signInFailure(data.message || "Login failed"));
    }
  } catch (error) {
    console.log("9. Error caught:", error.message);
    dispatch(signInFailure(error.message || "Something went wrong"));
  } finally {
    // Đảm bảo loading luôn được tắt nếu cần
    // dispatch(signInFailure(null)); // Có thể cần thêm logic để reset loading
  }
};
  // console.log(formData);
  return (
    <div className="min-h-screen flex items-center justify-center bg-white font-sans">
      <div className="w-full max-w-5xl flex flex-col md:flex-row items-center justify-center gap-8 p-4 md:p-8">
        {/* Form Section */}
        <div className="w-full md:w-1/2 max-w-md">
          <div className="text-center md:text-left mb-6">
            <h1 className="text-3xl font-bold text-gray-800">Welcome back!</h1>
            <p className="text-gray-600 mt-2">
              Enter your Credentials to access your account
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            {/* Email Field */}
            <div>
              <label className="block text-gray-700 text-sm font-medium mb-2">Email address</label>
              <input
                type="email"
                id="email_phone"
                value={formData.email_phone}
                onChange={handleChange}
                placeholder="Enter email"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
                required
              />
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-gray-700 text-sm font-medium mb-2">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  id="password"
                  value={formData.password}
                  onChange={handleChange}
                  placeholder="Enter password"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
                  required
                />
                <button
                  type="button"
                  onClick={toggleShowPassword}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500"
                >
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
              <div className="text-right mt-2">
                <Link to="/forgot-password" className="text-sm text-blue-600 hover:underline">
                  Forget password
                </Link>
              </div>
            </div>

            {/* Remember Me Checkbox */}
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-800">
                Remember for 30 days
              </label>
            </div>

            {/* Sign In Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3 bg-green-700 text-white rounded-lg hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-green-600 flex items-center justify-center"
            >
              {loading ? (
                <>
                  <Spinner size="sm" />
                  <span className="ml-2">Loading...</span>
                </>
              ) : (
                "Login"
              )}
            </button>

            {/* Error Message */}
            {errorMessage && (
              <Alert className="mt-4" color="failure">
                {errorMessage}
              </Alert>
            )}
          </form>

          {/* Divider */}
          <div className="flex items-center my-3 md:my-4">
            <div className="flex-grow border-t border-gray-300"></div>
            <span className="mx-4 text-gray-500">Or</span>
            <div className="flex-grow border-t border-gray-300"></div>
          </div>

          {/* Social Login Buttons */}
          <div className="space-y-3">
            <button
              type="button"
              className="w-full py-3 border border-gray-300 rounded-lg flex items-center justify-center gap-2 hover:bg-gray-50"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                viewBox="0 0 512 512"
              >
                <path
                  fill="#fbbd00"
                  d="M120 256c0-25.367 6.989-49.13 19.131-69.477v-86.308H52.823C18.568 144.703 0 198.922 0 256s18.568 111.297 52.823 155.785h86.308v-86.308C126.989 305.13 120 281.367 120 256z"
                />
                <path
                  fill="#0f9d58"
                  d="m256 392-60 60 60 60c57.079 0 111.297-18.568 155.785-52.823v-86.216h-86.216C305.044 385.147 281.181 392 256 392z"
                />
                <path
                  fill="#31aa52"
                  d="m139.131 325.477-86.308 86.308a260.085 260.085 0 0 0 22.158 25.235C123.333 485.371 187.62 512 256 512V392c-49.624 0-93.117-26.72-116.869-66.523z"
                />
                <path
                  fill="#3c79e6"
                  d="M512 256a258.24 258.24 0 0 0-4.192-46.377l-2.251-12.299H256v120h121.452a135.385 135.385 0 0 1-51.884 55.638l86.216 86.216a260.085 260.085 0 0 0 25.235-22.158C485.371 388.667 512 324.38 512 256z"
                />
                <path
                  fill="#cf2d48"
                  d="m352.167 159.833 10.606 10.606 84.853-84.852-10.606-10.606C388.668 26.629 324.381 0 256 0l-60 60 60 60c36.326 0 70.479 14.146 96.167 39.833z"
                />
                <path
                  fill="#eb4132"
                  d="M256 120V0C187.62 0 123.333 26.629 74.98 74.98a259.849 259.849 0 0 0-22.158 25.235l86.308 86.308C162.883 146.72 206.376 120 256 120z"
                />
              </svg>
              Sign in with Google
            </button>
          </div>

          {/* Sign Up Link */}
          <p className="text-center mt-6 text-gray-600">
            Don't have an account?{" "}
            <Link to="/register" className="text-blue-600 hover:underline">
              Sign Up
            </Link>
          </p>
        </div>

        {/* Image Section (Hidden on Mobile) */}
        <div className="hidden md:block w-1/2 h-[500px] rounded-lg overflow-hidden">
          <img
            src={background}
            alt="Background"
            className="w-full h-full object-cover"
          />
        </div>
      </div>
    </div>
  );
}