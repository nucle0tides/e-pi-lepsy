"use client";

import { useForm, SubmitHandler } from "react-hook-form";

type AddPetInputs = {
  firstName: string;
  lastName: string;
  householdId: number;
  dateOfBirth: string;
};

export function AddPetForm() {
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<AddPetInputs>();
  const onSubmit: SubmitHandler<AddPetInputs> = (data) => console.log(data);

  console.log(watch("firstName")); // watch input value by passing the name of it

  return (
    /* "handleSubmit" will validate your inputs before invoking "onSubmit" */
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* register your input into the hook by invoking the "register" function */}
      {/* include validation with required or other standard HTML validation rules */}
      <input {...register("firstName", { required: true })} />
      <input {...register("lastName", { required: true })} />
      <input {...register("householdId", { required: true })} />
      <input {...register("dateOfBirth", { required: true })} />
      {/* errors will return when field validation fails  */}
      {/* TODO: hilariously bad error checking */}
      {errors.firstName &&
        errors.lastName &&
        errors.householdId &&
        errors.dateOfBirth && <span>This field is required</span>}
      <input type="submit" />
    </form>
  );
}
