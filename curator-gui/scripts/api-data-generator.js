// Generate analytical report filled with random data

function getDataPoints(dataPoints) {
    return new Array(dataPoints).fill(0).map(() => Math.floor(Math.random() * 10000))
}

function generateAnalyticalReport(name, dataPoints) {
    return {
        namespace: name,
        cpu_usage: getDataPoints(dataPoints),
        network_usage: getDataPoints(dataPoints),
        memory_usage: getDataPoints(dataPoints)
    }
}

function generate(dataPoints, freq) {
    const names = ["openshift-apiserver", "openshift-apiserver-operator", "openshift-authentication", "openshift-authentication-operator", "openshift-cluster-machine-approver", "openshift-cluster-node-tuning-operator", "openshift-cluster-samples-operator", "openshift-cluster-version", "openshift-config-operator", "openshift-console", "openshift-console-operator", "openshift-controller-manager", "openshift-controller-manager-operator", "openshift-dns", "openshift-dns-operator", "openshift-etcd", "openshift-etcd-operator", "openshift-image-registry", "openshift-ingress", "openshift-ingress-operator", "openshift-kube-apiserver", "openshift-kube-apiserver-operator", "openshift-kube-controller-manager", "openshift-kube-controller-manager-operator", "openshift-kube-scheduler", "openshift-kube-storage-version-migrator", "openshift-marketplace", "openshift-metering", "openshift-monitoring", "openshift-multus", "openshift-network-operator", "openshift-operator-lifecycle-manager", "openshift-sdn", "openshift-service-ca", "openshift-service-ca-operator"];
    return {
      reports: names.map(name => generateAnaReport(name, dataPoints)),
      request_parameters: {"start":"10/22/2019","frequency":freq}
    }
}
