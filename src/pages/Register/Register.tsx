import React from "react";
import background from '../../assets/image/cut.png';
import {Link} from 'react-router-dom'

export default function Register() {
  return (
    <div className="font-[sans-serif]">
      <div className="flex flex-col items-center justify-center w-full h-screen">
        <div className="grid md:grid-cols-2 items-center gap-4 max-md:gap-8 max-w-full w-full h-full m-0 rounded-md flex-col items-center justify-center">
          <div className="flex flex-col items-center justify-center">
            <div className="m-3 md:max-w-md w-full flex flex-col items-center justify-center">
                <form className="w-full max-w-sm">
                  <div className="mb-12 flex flex-col items-center justify-center">
                    <h3 className="text-gray-800 text-4xl font-bold">Get Started Now</h3>
                  </div>

                  <div className="grid grid-cols-2 flex flex-col items-center justify-center">
                    <div className="mr-1.5">
                      <label className="text-gray-800 text-xs block">First Name</label>
                      <div className="relative flex items-center">
                        <input name="firstName" type="text" required className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" placeholder="First name" />
                      </div>
                    </div>

                    <div className="ml-1.5">
                      <label className="text-gray-800 text-xs block">Last Name</label>
                      <div className="relative flex items-center">
                        <input name="lastName" type="text" required className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" placeholder="Last name" />
                      </div>
                    </div>
                  </div>

                  <div className="mt-2">
                    <label className="text-gray-800 text-xs block">User Name</label>
                    <div className="relative flex items-center">
                      <input name="userName" type="text" required className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" placeholder="User name" />
                    </div>
                  </div>


                  <div className="mt-2">
                    <label className="text-gray-800 text-xs block">Password</label>
                    <div className="relative flex items-center">
                      <input name="password" type="password" required className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" placeholder="Enter password" />
                      {/* <svg xmlns="http://www.w3.org/2000/svg" fill="#bbb" stroke="#bbb" className="w-[18px] h-[18px] absolute right-2 cursor-pointer" viewBox="0 0 128 128">
                        <path d="M64 104C22.127 104 1.367 67.496.504 65.943a4 4 0 0 1 0-3.887C1.367 60.504 22.127 24 64 24s62.633 36.504 63.496 38.057a4 4 0 0 1 0 3.887C126.633 67.496 105.873 104 64 104zM8.707 63.994C13.465 71.205 32.146 96 64 96c31.955 0 50.553-24.775 55.293-31.994C114.535 56.795 95.854 32 64 32 32.045 32 13.447 56.775 8.707 63.994zM64 88c-13.234 0-24-10.766-24-24s10.766-24 24-24 24 10.766 24 24-10.766 24-24 24zm0-40c-8.822 0-16 7.178-16 16s7.178 16 16 16 16-7.178 16-16-7.178-16-16-16z" data-original="#000000"></path>
                      </svg> */}
                    </div>
                  </div>

                  <div className="grid grid-cols-2 flex flex-col items-center justify-center mt-1.5">
                    <div className="mr-1.5">
                      <label className="text-gray-800 text-xs block">Email</label>
                      <div className="relative flex items-center">
                        <input name="email" type="text" required className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" placeholder="Email" />
                      </div>
                    </div>

                    <div className="ml-1.5">
                      <label className="text-gray-800 text-xs block">Phone Number</label>
                      <div className="relative flex items-center">
                        <input name="phoneNumber" type="text" required className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" placeholder="Address" />
                      </div>
                    </div>
                  </div>


                  <div className="mt-2">
                    <label className="text-gray-800 text-xs block">Address</label>
                    <div className="relative flex items-center">
                      <input name="adress" type="text" required className="w-full text-gray-800 text-sm border-b border-gray-300 focus:border-blue-600 px-2 py-3 outline-none" placeholder="Address" />
                    </div>
                  </div>


                  <div className="flex flex-wrap items-center justify-between gap-4 mt-6">
                    <div className="flex items-center">
                      <input id="remember-me" name="remember-me" type="checkbox" className="h-4 w-4 shrink-0 text-blue-600 focus:ring-blue-500 border-gray-300 rounded" />
                      <label htmlFor="remember-me" className="mt-1 ml-2 block text-sm text-gray-800 font-semibold">
                        I agree to the terms & policy
                      </label>
                    </div>
                  </div>

                  <div className="mt-8">
                    <button type="button" className="w-full shadow-xl py-1 px-4 text-sm tracking-wide rounded-md text-white bg-green-700 hover:bg-green-800 focus:outline-none">
                      Register
                    </button>
                  </div>

                  <div className="flex items-center justify-center mt-9 mb-2">
                    <div className="flex-grow border-t border-gray-300"></div>
                    <span className="mx-4 text-black-500">Or</span>
                    <div className="flex-grow border-t border-gray-300"></div>
                  </div>

                  <div className="flex flex-col items-center justify-between">
                    <div className="flex items-center justify-between">
                      <label htmlFor="remember-me" className="mr-2 block text-sm text-gray-800 font-semibold">
                        Have an account?
                      </label>
                      <Link to="/login" className="text-blue-600 font-semibold text-sm hover:underline">
                        Sign In?
                      </Link>
                    </div>
                   
                  </div>

                </form>

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