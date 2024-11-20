"use client";

import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import Image from "next/image";
import Link from "next/link";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "./ui/select";
import { Eye, EyeClosed } from "lucide-react";
import AvatarUploader from "./AvatarUploader";

type FormType = "login" | "register";

const authFormSchema = (formType: FormType) => {
  return z.object({
    email: z.string().email(),
    password: z.string().min(8),
    names:
      formType === "register"
        ? z.string().min(2).max(50)
        : z.string().optional(),
    role:
      formType === "register"
        ? z.string().min(2).max(50)
        : z.string().optional(),
    avatar: formType === "register" ? z.string().url() : z.string().optional(),
  });
};

export default function AuthForm({ type }: { type: FormType }) {
  const [isLoading, setIsLoading] = useState(false);
  const [isPassword, setIsPassword] = useState(true);

  const formSchema = authFormSchema(type);
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      names: "",
      email: "",
      role: "",
      avatar: "",
      password: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    try {
      console.log(values);
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="auth-form">
          <h1 className="form-title">
            {type === "login"
              ? "Login to your account"
              : "Register your account"}
          </h1>
          {type === "register" && (
            <>
              <FormField
                name="names"
                control={form.control}
                render={({ field }) => (
                  <FormItem>
                    <div className="shad-form-item">
                      <FormLabel className="shad-form-label">
                        Full Name
                      </FormLabel>
                      <FormControl>
                        <Input
                          placeholder="Enter your full names"
                          className="shad-input"
                          {...field}
                        />
                      </FormControl>
                    </div>
                    <FormMessage className="shad-form-message" />
                  </FormItem>
                )}
              />
              <FormField
                name="role"
                control={form.control}
                render={({ field }) => (
                  <FormItem>
                    <div className="shad-form-item">
                      <FormLabel className="shad-form-label">Role</FormLabel>
                      <FormControl>
                        <Select {...field}>
                          <SelectTrigger className="w-full border-none px-4 py-2 outline-none">
                            <SelectValue placeholder="User" />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="admin">Admin</SelectItem>
                            <SelectItem value="staff">Staff</SelectItem>
                            <SelectItem value="user">User</SelectItem>
                          </SelectContent>
                        </Select>
                      </FormControl>
                    </div>
                    <FormMessage className="shad-form-message" />
                  </FormItem>
                )}
              />
              <FormField
                name="avatar"
                control={form.control}
                render={({field}) => (
                  <FormItem>
                    <div className="shad-form-item">
                      <FormLabel className="shad-form-label">Avatar</FormLabel>
                      <FormControl>
                        <AvatarUploader file={form.getValues("avatar")} onChange={field.onChange}/>
                      </FormControl>
                    </div>
                    <FormMessage className="shad-form-message"/>
                  </FormItem>
                )}
              />
            </>
          )}
          <FormField
            name="email"
            control={form.control}
            render={({ field }) => (
              <FormItem>
                <div className="shad-form-item">
                  <FormLabel className="shad-form-label">Email</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Enter your email"
                      className="shad-input"
                      {...field}
                    />
                  </FormControl>
                </div>
                <FormMessage className="shad-form-message" />
              </FormItem>
            )}
          />
          <FormField
            name="password"
            control={form.control}
            render={({ field }) => (
              <FormItem>
                <div className="shad-form-item">
                  <FormLabel className="shad-form-label">Password</FormLabel>
                  <FormControl>
                    <div className="flex justify-between items-center">
                      <Input
                        type={isPassword ? "password" : "text"}
                        className="shad-input"
                        {...field}
                      />
                      <span onClick={() => setIsPassword(!isPassword)}>
                        {isPassword ? <EyeClosed /> : <Eye />}
                      </span>
                    </div>
                  </FormControl>
                </div>
                <FormMessage className="shad-form-message" />
              </FormItem>
            )}
          />
          <Button
            type="submit"
            className="form-submit-button"
            disabled={isLoading}
          >
            {type === "register" ? "Sign Up" : "Sign In"}
            {isLoading && (
              <Image
                src="/assets/icons/loader.svg"
                alt="loader"
                width={24}
                height={24}
                className="ml-2 animate-spin"
              />
            )}
          </Button>
          <div className="body-2 flex justify-center">
            <p className="text-light-100">
              {type === "login"
                ? "Already have an account ?"
                : "Don't have an account ?"}
              <Link
                href={type === "login" ? "/register" : "/login"}
                className="ml-1 font-medium text-brand"
              >
                {type === "login" ? "Register here" : "Login here"}
              </Link>
            </p>
          </div>
        </form>
      </Form>
    </>
  );
}
