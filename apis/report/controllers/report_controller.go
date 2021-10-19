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

package controllers

import (
	"context"
	"fmt"
	//v1 "k8s.io/api/batch/v1"
	//metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"strings"

	"github.com/go-logr/logr"
	"k8s.io/apimachinery/pkg/runtime"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/log"

	batchv1 "curator.openshift.io/guestbook/api/v1"
	v1beta1 "k8s.io/api/batch/v1beta1"
	"k8s.io/client-go/kubernetes/scheme"
)

// ReportReconciler reconciles a Report object
type ReportReconciler struct {
	client.Client
	Log    logr.Logger
	Scheme *runtime.Scheme
}

//+kubebuilder:rbac:groups=batch.curator.openshift.io,resources=reports,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=batch.curator.openshift.io,resources=reports/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=batch.curator.openshift.io,resources=reports/finalizers,verbs=update

// Reconcile is part of the main kubernetes reconciliation loop which aims to
// move the current state of the cluster closer to the desired state.
// TODO(user): Modify the Reconcile function to compare the state specified by
// the Report object against the actual cluster state, and then
// perform operations to make the cluster state reflect the state specified by
// the user.
//
// For more details, check Reconcile and its Result here:
// - https://pkg.go.dev/sigs.k8s.io/controller-runtime@v0.8.3/pkg/reconcile
func (r *ReportReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	_ = log.FromContext(ctx)

	// your logic here
// 	var report batchv1.Report
// 	if err := r.Get(ctx, req.NamespacedName, &report); err != nil {
// 		//log.Error(err, "unable to fetch CronJob")
// 		// we'll ignore not-found errors, since they can't be fixed by an immediate
// 		// requeue (we'll need to wait for a new notification), and we can get them
// 		// on deleted requests.
// 		//return ctrl.Result{}, client.IgnoreNotFound(err)
// 		return ctrl.Result{}, err
// 	}
// 	period := strings.ToLower(string(report.Spec.ReportPeriod))
// 	fmt.Print("get" + period)
// 	reportYaml := fmt.Sprintf(`
// apiVersion: batch/v1beta1
// kind: CronJob
// metadata:
//   name: %[1]vreport
// spec:
//   schedule: "05 0 * * *"  #  At 00:00
//   jobTemplate:
//     spec:
//       template:
//         spec:
//           volumes:
//             - name: backup-scripts
//               configMap:
//                 name: backup-scripts
//           initContainers:
//           - name: %[1]vreport
//             image: docker.io/library/postgres:13.0
//             imagePullPolicy: IfNotPresent
//             envFrom:
//               - configMapRef:
//                   name: backup-config
//             command:
//               - sh
//               - -c
//               - psql -d "postgresql://$DATABASE_USER:$DATABASE_PASSWORD@$DATABASE_HOST_NAME:$PORT_NUMBER/$DATABASE_NAME" -c "SELECT generate_report('%[1]v');"
//           containers:
//             - name: %[1]vemail
//               image: quay.io/operate-first/curator-s3-sync:latest
//               imagePullPolicy: IfNotPresent
//               envFrom:
//                 - secretRef:
//                     name: email-credentials
//                 - configMapRef:
//                     name: backup-config
//               command:
//                 - python3
//                 - /scripts/send_email.py
//                 - %[1]v
//               volumeMounts:
//                 - name: backup-scripts
//                   mountPath: /scripts
//           restartPolicy: Never
//           backoffLimit: 0`, period)
// 	decode := scheme.Codecs.UniversalDeserializer().Decode
// 	obj, _, err := decode([]byte(reportYaml), nil, nil)
// 	if err != nil {
// 		fmt.Printf("%#v", err)
// 		return ctrl.Result{}, err
// 	}
//
// 	cronjob := obj.(*v1beta1.CronJob)
// 	cronjob.Spec.Schedule = report.Spec.Schedule
// 	_, err = ctrl.CreateOrUpdate(ctx, r.Client, cronjob, func() error {
// 		return ctrl.SetControllerReference(&report, cronjob, r.Scheme)
// 	}) // idempotent
// 	if err != nil {
// 		fmt.Printf("%#v", err)
// 		return ctrl.Result{}, err
// 	}
// 	fmt.Print("finished")
// 	//var childJobs kbatch.JobList
// 	//if err := r.List(ctx, &childJobs, client.InNamespace(req.Namespace), client.MatchingFields{jobOwnerKey: req.Name}); err != nil {
// 	//	log.Error(err, "unable to list child Jobs")
// 	//	return ctrl.Result{}, err
// 	//}
	return ctrl.Result{}, nil
}

// SetupWithManager sets up the controller with the Manager.
func (r *ReportReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&batchv1.Report{}).
		Complete(r)
}
