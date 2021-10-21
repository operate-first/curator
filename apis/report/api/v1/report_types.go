/*
Copyright 2021.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

package v1

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// EDIT THIS FILE!  THIS IS SCAFFOLDING FOR YOU TO OWN!
// NOTE: json tags are required.  Any new fields you add must have json tags for the fields to be serialized.

// ReportSpec defines the desired state of Report
type ReportSpec struct {
	// INSERT ADDITIONAL SPEC FIELDS - desired state of cluster
	// Important: Run "make" to regenerate code after modifying this file

	//+kubebuilder:validation:MinLength=0
	// The schedule in Cron format, see https://en.wikipedia.org/wiki/Cron.
	// +optional
	Schedule string `json:"schedule"`

	// ReportingEnd specifies the time this Report should end
	ReportingEnd *metav1.Time `json:"reportingEnd"`

	// ReportingStart specifies the time this Report should start from
	// This is intended for allowing a Report to start from the past
	// +optional
	ReportingStart *metav1.Time `json:"reportingStart"`

	// Specifies how to treat concurrent executions of a Job.
	// Valid values are:
	// - "Day" (default): daily (24 hrs) report ends on ReportingEnd;
	// - "Week": weekly (7 days) report ends on ReportingEnd;
	// - "Month": monthly (30 calendar days) report ends on ReportingEnd
	// +optional
	ReportPeriod ReportPeriod `json:"reportPeriod,omitempty"`

	//+kubebuilder:validation:MinLength=0
	// +optional

	Namespace string `json:"namespace"`

	// RunImmediately will run the report immediately, ignoring ReportingStart
	// and, ReportingEnd.
	//RunImmediately bool `json:"runImmediately,omitempty"`
}

// Only one of the following choice may be specified.
// If none of the following policies is specified, the default one
// is DailyReport.
// +kubebuilder:validation:Enum=Day;Week;Month
type ReportPeriod string

const (
	// AllowConcurrent allows CronJobs to run concurrently.
	Daily ReportPeriod = "Day"

	// ForbidConcurrent forbids concurrent runs, skipping next run if previous
	// hasn't finished yet.
	Weekly ReportPeriod = "Week"

	// ReplaceConcurrent cancels currently running job and replaces it with a new one.
	Monthly ReportPeriod = "Month"
)

// ReportStatus defines the observed state of Report
type ReportStatus struct {
	// INSERT ADDITIONAL STATUS FIELD - define observed state of cluster
	// Important: Run "make" to regenerate code after modifying this file
	// Information when was the last time the report was successfully generated.
	// +optional
	LastScheduleTime *metav1.Time `json:"lastScheduleTime,omitempty"`

	Conditions string `json:"conditions,omitempty"`
}

//+kubebuilder:object:root=true
//+kubebuilder:subresource:status

// Report is the Schema for the reports API
type Report struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   ReportSpec   `json:"spec,omitempty"`
	Status ReportStatus `json:"status,omitempty"`
}

//+kubebuilder:object:root=true

// ReportList contains a list of Report
type ReportList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []Report `json:"items"`
}

func init() {
	SchemeBuilder.Register(&Report{}, &ReportList{})
}
