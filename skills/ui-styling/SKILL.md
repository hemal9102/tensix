---
name: ui-styling
description: Constructs accessible user interfaces using shadcn/ui components (Radix UI + Tailwind CSS) and utility-first styling. Use when building React/Next.js frontend layouts, adding interactive components (dialogs, data tables, form validation), or implementing dark mode. Do NOT use for raw logo design or server-side API logic.
---

# Front-End UI Styling & Component Engineering

Comprehensive system for building accessible, modern web user interfaces using shadcn/ui primitives and Tailwind CSS utilities.

## Core Stack Integration
- **Component Layer**: shadcn/ui primitives built on Radix UI for accessibility (WAI-ARIA compliance).
- **Styling Layer**: Tailwind CSS utility classes and design tokens.
- **State & Validation**: React Hook Form with Zod schema resolution.

---

## Component Setup & Patterns

### 1. Component Initialization
```bash
# Add shadcn/ui components
npx shadcn@latest add button card dialog form input
```

### 2. Form Implementation Pattern
```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Form, FormField, FormItem, FormLabel, FormControl, FormMessage } from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

const schema = z.object({
  email: z.string().email(),
})

export function ContactForm() {
  const form = useForm({ resolver: zodResolver(schema), defaultValues: { email: "" } })

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit((d) => console.log(d))} className="space-y-4">
        <FormField control={form.control} name="email" render={({ field }) => (
          <FormItem>
            <FormLabel>Email Address</FormLabel>
            <FormControl><Input type="email" {...field} /></FormControl>
            <FormMessage />
          </FormItem>
        )} />
        <Button type="submit" className="w-full">Submit</Button>
      </form>
    </Form>
  )
}
```

---

## Rules of Engagement

#### ✅ Do
- Build mobile-first using Tailwind responsive prefixes (`sm:`, `md:`, `lg:`).
- Support dark mode using standard Tailwind `dark:` variant classes.
- Ensure focus states are accessible (`focus-visible:outline-none focus-visible:ring-2`).

#### ❌ Don't
- Do NOT construct custom dynamic CSS class names via string concatenation (use `cn()` utility).
- Do NOT bypass Radix accessibility primitives for complex overlays (dialogs, dropdowns).
- Do NOT write inline styles; utilize Tailwind utility classes.

---

## Verification & Grounding Loop

1. **Accessibility Check**: Confirm keyboard trap-free navigation and WAI-ARIA compliance.
2. **Build Verification**: Run TypeScript check and linter to verify zero component prop mismatches:
   ```bash
   npx tsc --noEmit
   ```
