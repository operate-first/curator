import * as React from 'react';
import { Form, FormGroup, ActionGroup, FormHelperText } from '@patternfly/react-core/src/components/Form'
import { TextInput } from '@patternfly/react-core/src/components/TextInput';
import { Button } from '@patternfly/react-core/src/components/Button';
import { ValidatedOptions } from '@patternfly/react-core/src/helpers/constants';

export interface LoginFormProps extends React.HTMLProps<HTMLFormElement> {
    /** Flag to indicate if the first dropdown item should not gain initial focus */
    noAutoFocus?: boolean;
    /** Additional classes added to the Login Main Body's Form */
    className?: string;
    /** Flag indicating the Helper Text is visible * */
    showHelperText?: boolean;
    /** Content displayed in the Helper Text component * */
    helperText?: React.ReactNode;
    /** Icon displayed to the left in the Helper Text */
    helperTextIcon?: React.ReactNode;
    /** Label for the Username Input Field */
    oldPasswordLabel?: string;
    /** Value for the Username */
    oldPasswordValue?: string;
    onChangeOldPassword?: (value: string, event: React.FormEvent<HTMLInputElement>) => void;
    /** Function that handles the onChange event for the Username */
    onBlurOldPasswordValue?: (event: React.FocusEvent<HTMLInputElement>) => void;
    /** Flag indicating if the Username is valid */
    isValidUsername?: boolean;
    /** Label for the Password Input Field */
    newPasswordLabel?: string;
    confirmPasswordLabel?: string;
    /** Value for the Password */
    newPasswordValue?: string;
    confirmPasswordValue?: string;
    /** Function that handles the onChange event for the Password */
    onChangeNewPassword?: (value: string, event: React.FormEvent<HTMLInputElement>) => void;
    onChangeConfirmPassword?: (value: string, event: React.FormEvent<HTMLInputElement>) => void;
    /** Flag indicating if the Password is valid */
    isValidPassword?: boolean;
    /** Label for the Log in Button Input */
    resetButtonLabel?: string;
    /** Flag indicating if the Login Button is disabled */
    isResetButtonDisabled?: boolean;
    /** Function that is called when the Login button is clicked */
    onLoginButtonClick?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
    onResetButtonClick?: (event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
    /** Label for the Remember Me Checkbox that indicates the user should be kept logged in.  If the label is not provided, the checkbox will not show. */
    rememberMeLabel?: string;
    /** Flag indicating if the remember me Checkbox is checked. */
    isRememberMeChecked?: boolean;
    /** Function that handles the onChange event for the Remember Me Checkbox */
    onChangeRememberMe?: (checked: boolean, event: React.FormEvent<HTMLInputElement>) => void;
}

export const ResetPasswordForm: React.FunctionComponent<LoginFormProps> = ({
    noAutoFocus = false,
    className = '',
    showHelperText = false,
    helperText = null,
    helperTextIcon = null,
    oldPasswordLabel = 'Old Password',
    oldPasswordValue = '',
    onChangeOldPassword = () => undefined as any,
    onBlurOldPasswordValue = () => undefined as any,
    isValidUsername = true,
    newPasswordLabel = 'New Password',
    newPasswordValue = '',
    confirmPasswordLabel = 'Confirm New Password',
    confirmPasswordValue = '',
    onChangeNewPassword = () => undefined as any,
    onChangeConfirmPassword = () => undefined as any,
    isValidPassword = true,
    resetButtonLabel = 'Reset Password',
    isResetButtonDisabled = false,
    onLoginButtonClick = () => undefined as any,
    onResetButtonClick = () => undefined as any,
    rememberMeLabel = '',
    isRememberMeChecked = false,
    onChangeRememberMe = () => undefined as any,
    ...props
}: LoginFormProps) => (
        <Form className={className} {...props}>
            <FormHelperText isError={!isValidUsername || !isValidPassword} isHidden={!showHelperText} icon={helperTextIcon}>
                {helperText}
            </FormHelperText>
            <FormGroup
                label={oldPasswordLabel}
                isRequired
                validated={isValidUsername ? ValidatedOptions.default : ValidatedOptions.error}
                fieldId="pf-login-username-id"
            >
                <TextInput
                    autoFocus={!noAutoFocus}
                    id="pf-login-username-id"
                    isRequired
                    validated={isValidUsername ? ValidatedOptions.default : ValidatedOptions.error}
                    type="text"
                    name="pf-login-username-id"
                    value={oldPasswordValue}
                    onChange={onChangeOldPassword}
                    onBlur={onBlurOldPasswordValue}
                />
            </FormGroup>
            <FormGroup
                label={newPasswordLabel}
                isRequired
                validated={isValidPassword ? ValidatedOptions.default : ValidatedOptions.error}
                fieldId="pf-login-password-id"
            >
                <TextInput
                    isRequired
                    type="password"
                    id="pf-login-password-id"
                    name="pf-login-password-id"
                    validated={isValidPassword ? ValidatedOptions.default : ValidatedOptions.error}
                    value={newPasswordValue}
                    onChange={onChangeNewPassword}
                />
            </FormGroup>
            <FormGroup
                label={confirmPasswordLabel}
                isRequired
                validated={isValidPassword ? ValidatedOptions.default : ValidatedOptions.error}
                fieldId="pf-login-password-id"
            >
                <TextInput
                    isRequired
                    type="password"
                    id="pf-login-password-id"
                    name="pf-login-password-id"
                    validated={isValidPassword ? ValidatedOptions.default : ValidatedOptions.error}
                    value={confirmPasswordValue}
                    onChange={onChangeConfirmPassword}
                />
            </FormGroup>
            <ActionGroup>
                <Button variant="primary" type="submit" onClick={onLoginButtonClick} isBlock isDisabled={isResetButtonDisabled}>
                    {resetButtonLabel}
                </Button>
                <a href="#" onClick={onResetButtonClick} style={{ paddingLeft: "40%" }}>Login</a>
            </ActionGroup>
        </Form>
    );
